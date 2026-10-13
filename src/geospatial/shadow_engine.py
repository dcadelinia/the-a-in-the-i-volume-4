import math
from typing import Dict, List, Tuple
from shapely.geometry import Point, Polygon
from shapely.ops import transform
import pyproj

class ShadowEngine:
    """
    Geospatial computational layer for Project Koridor (Odynex Axis Logistics LLC).
    Calculates Atypical Air Environment (AAE) boundaries around vertical structures.
    """
    def __init__(self, base_safety_buffer_meters: float = 30.0):
        self.buffer_meters = base_safety_buffer_meters
        # WGS84 to Pseudo-Mercator projection for accurate metric buffering
        self.wgs84 = pyproj.CRS('EPSG:4326')
        self.mercator = pyproj.CRS('EPSG:3857')
        self.project_to_metric = pyproj.Transformer.from_crs(self.wgs84, self.mercator, always_xy=True).transform
        self.project_to_wgs84 = pyproj.Transformer.from_crs(self.mercator, self.wgs84, always_xy=True).transform

    def generate_structural_shadow(self, lat: float, lon: float, structure_height_meters: float) -> List[Tuple[float, float]]:
        """
        Creates a polygon tracking the safe 'airspace shadow zone' around a structural pillar.
        Dynamically factors structure height to calculate localized descent safety layers.
        """
        # Create structural origin point
        wgs_point = Point(lon, lat)
        metric_point = transform(self.project_to_metric, wgs_point)
        
        # Buffer distance scale relative to infrastructure heights
        dynamic_buffer = self.buffer_meters + (structure_height_meters * 0.15)
        shadow_polygon_metric = metric_point.buffer(dynamic_buffer)
        
        # Transform back to standard global GPS coordinates
        shadow_polygon_wgs = transform(self.project_to_wgs84, shadow_polygon_metric)
        return list(shadow_polygon_wgs.exterior.coords)

    def verify_route_compliance(self, route_points: List[Tuple[float, float]], allowed_zones: List[List[Tuple[float, float]]]) -> bool:
        """
        Confirms if a drone's programmed autonomous path sits entirely inside safe infrastructure shadows.
        """
        if not route_points or not allowed_zones:
            return False
            
        # Convert allowed zones to polygon spaces
        safe_polygons = [Polygon(zone) for zone in allowed_zones]
        
        for pt in route_points:
            point = Point(pt[1], pt[0]) # Lon, Lat conversion
            inside_any_shadow = any(poly.contains(point) for poly in safe_polygons)
            if not inside_any_shadow:
                return False # Detected a segment breaching open airspace
        return True
