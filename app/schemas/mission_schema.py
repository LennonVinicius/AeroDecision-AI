from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class MissionRequest(BaseModel):
    origin_airport: str
    destination_airport: str
    mission_type: str
    priority: str
    passengers: int
    distance_km: float | None = None
    cargo_weight: float
    estimated_flight_time: float | None = None
    weather_condition: str | None = None
    required_runway: str | None = None
    budget: float | None = None

class MissionResponse(BaseModel):
    id: int
    origin_airport: str
    destination_airport: str
    mission_type: str
    priority: str
    passengers: int
    cargo_weight: float
    distance_km: float
    created_at: datetime
    best_aircraft: Optional[str] = None
    mission_time: Optional[float] = None
    total_cost: Optional[float] = None

    class Config:
        from_attributes = True