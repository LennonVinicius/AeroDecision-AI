from fastapi import APIRouter
from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.schemas.aircraft_schema import AircraftResponse
from typing import List
router = APIRouter(prefix="/fleet")

@router.get("/get_fleet", response_model=list[AircraftResponse])
def get_fleet():
    db = sessionLocal()
    try:
        fleet = db.query(Aircraft).all()
        return fleet 
    finally:
        db.close()
    