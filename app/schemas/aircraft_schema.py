from pydantic import BaseModel

class AircraftResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    family: str
    aircraft_type: str

    class Config:
        from_attributes = True 