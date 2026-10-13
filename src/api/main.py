from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from src.geospatial.shadow_engine import ShadowEngine

app = FastAPI(
    title="Project Koridor API - Odynex Axis Logistics LLC",
    description="Automated routing and Atypical Air Environment (AAE) analytics engine for SOWEGA precision agrilogistics.",
    version="1.0.0"
)

# Instantiate engine core
engine = ShadowEngine(base_safety_buffer_meters=30.0)

class StructureLog(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    height_meters: float

class PathEvaluationRequest(BaseModel):
    flight_plan: List[Tuple[float, float]]  # List of [lat, lon]
    infrastructure_nodes: List[StructureLog]

@app.get("/")
def read_root():
    return {
        "company": "Odynex Axis Logistics LLC",
        "initiative": "The A in the I: Volume 4",
        "system_status": "ONLINE"
    }

@app.post("/api/v1/evaluate-path")
def evaluate_flight_path(request: PathEvaluationRequest):
    try:
        # Step 1: Calculate active structural shadows from inputs
        allowed_shadow_polygons = []
        for node in request.infrastructure_nodes:
            poly_coords = engine.generate_structural_shadow(
                lat=node.latitude, 
                lon=node.longitude, 
                structure_height_meters=node.height_meters
            )
            allowed_shadow_polygons.append(poly_coords)
            
        # Step 2: Validate compliance status
        is_compliant = engine.verify_route_compliance(
            route_points=request.flight_plan, 
            allowed_zones=allowed_shadow_polygons
        )
        
        return {
            "compliant_with_aae_shielding": is_compliant,
            "mapped_zones_count": len(allowed_shadow_polygons),
            "recommendation": "AUTHORIZED" if is_compliant else "REJECTED_OPEN_AIRSPACE_RISK"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
