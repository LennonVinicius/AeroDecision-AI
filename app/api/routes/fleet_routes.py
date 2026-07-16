from fastapi import APIRouter
from app.schemas.aircraft_schema import AircraftResponse
from app.services.aircraft_service import Aircraftservice
from typing import List
router = APIRouter(prefix="/fleet")

@router.get("/get_fleet", response_model=List[AircraftResponse])
def get_fleet_total():
    aircraft_service =  Aircraftservice()
    lista = aircraft_service.get_fleet()
    print(lista)
    return lista