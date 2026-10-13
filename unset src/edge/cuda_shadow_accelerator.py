import numpy as np
try:
    import cupy as cp
    HAS_CUDA = True
except ImportError:
    # Fallback to standard numpy if running on non-GPU prototyping machine
    import numpy as cp
    HAS_CUDA = False

class CUDAShadowAccelerator:
    """
    Hardware-accelerated validation layer utilizing NVIDIA CUDA processing elements.
    Optimized for multi-swarm waypoint calculations at sub-millisecond frequencies.
    """
    def __init__(self):
        self.cuda_enabled = HAS_CUDA

    def batch_verify_points(self, route_points_matrix: np.ndarray, shadow_bounds_matrix: np.ndarray) -> np.ndarray:
        """
        Processes parallel ray-casting or point-in-polygon math on the GPU.
        route_points_matrix: Shape (N, 2) containing [Lat, Lon] arrays
        shadow_bounds_matrix: Shape (M, 4) containing bounding boxes [MinLat, MinLon, MaxLat, MaxLon]
        Returns a boolean array mapping which points are safe within an infrastructure shadow.
        """
        if self.cuda_enabled:
            # Shift raw array matrices from Host (CPU Memory) to Device (GPU VRAM)
            d_points = cp.asarray(route_points_matrix)
            d_shadows = cp.asarray(shadow_bounds_matrix)
        else:
            d_points = route_points_matrix
            d_shadows = shadow_bounds_matrix

        # Extract coordinate slices across parallel structures
        p_lat = d_points[:, 0, None]
        p_lon = d_points[:, 1, None]
        
        s_min_lat = d_shadows[None, :, 0]
        s_min_lon = d_shadows[None, :, 1]
        s_max_lat = d_shadows[None, :, 2]
        s_max_lon = d_shadows[None, :, 3]

        # Parallel Vector Matrix Verification Math (Executed across active CUDA threads)
        inside_condition = (p_lat >= s_min_lat) & (p_lat <= s_max_lat) & \
                           (p_lon >= s_min_lon) & (p_lon <= s_max_lon)
                           
        # Check if each individual coordinate fits inside at least one infrastructure shadow zone
        point_safety_mask = cp.any(inside_condition, axis=1)

        if self.cuda_enabled:
            # Pull completed calculations back down to host memory space
            return cp.asnumpy(point_safety_mask)
        return point_safety_mask
