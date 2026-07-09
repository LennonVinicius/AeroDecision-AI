from pydantic import BaseModel

class MissionRequest(BaseModel):

    origin_airport: str

    destination_airport: str

    passengers: int

    cargo_weight: float

    priority: str