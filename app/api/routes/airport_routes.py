from fastapi import APIRouter
from app.db.database import sessionLocal
from app.db.entities import Airport
from typing import List
from app.schemas.airport_schema import AirportResponse
router = APIRouter(prefix="/airports")

@router.get("/get_airports", response_model=List[AirportResponse])
def get_airports():
    db = sessionLocal()
    try:
        airports = db.query(Airport).all()
        return airports    
    finally:
        db.close()
@router.get("/search")
def search_airports(q: str):
    db = sessionLocal()
    try:
        airports = (
            db.query(Airport).filter(
                Airport.icao.ilike(f"%{q}%")|
                Airport.iata.ilike(f"%{q}%")|
                Airport.name.ilike(f"%{q}%")|
                Airport.city.ilike(f"%{q}%")
            ).limit(10).all()
        )
        return[{
                "icao": airport.icao,
                "iata": airport.iata,
                "name": airport.name,
                "city": airport.city,
                "country": airport.country
            }
            for airport in airports
        ]
    finally:
        db.close()
    