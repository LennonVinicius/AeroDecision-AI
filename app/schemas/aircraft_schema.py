from pydantic import BaseModel

class AircraftResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    family: str
    aircraft_type: str
    range_km: float
    max_passengers: int
    operational_cost_hour: float
    class Config:
        from_attributes = True 

