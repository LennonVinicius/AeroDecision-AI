from pydantic import BaseModel

class AirportResponse(BaseModel):
    id: int
    icao: str
    iata: str
    name: str
    latitude: float
    longitude: float
    city: str
    country: str
    runway_length: float
    
    class Config:
        from_attributes = True 