from pydantic import BaseModel

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
