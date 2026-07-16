from pydantic import BaseModel
from datetime import datetime
class MissionRequest(BaseModel):
    origin_airport: str
    destination_airport: str
    mission_type: str
    priority: str
    passengers: int
    distance_km: float | None = None
    cargo_weight: float
    created_at: datetime
    estimated_flight_time: float | None = None
    weather_condition: str | None = None
    required_runway: str | None = None
    budget: float | None = None
    best_aircraft : str
    mission_time : float
    total_cost: float
