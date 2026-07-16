from fastapi import APIRouter
from app.db.database import sessionLocal
from app.db.entities import Mission
from app.db.entities import Aircraft
from app.services.aircraft_service import Aircraftservice
from app.services.cost_service import CostService
from app.services.mission_service import MissionService
import datetime
from datetime import datetime
router = APIRouter(prefix="/dashboard")


@router.get("/get_missions_month")
def get_missions_month():   
    mission_service = MissionService()
    result = mission_service.get_mission_month()
    return result

@router.get("/get_most_used_aircraft")
def get_most_used_aircraft():
    aircraft_service = Aircraftservice()
    result = aircraft_service.most_used_aircraft()
    return result
@router.get("/cost")
def cost_per_mission():
    cost_service = CostService()
    result = cost_service.cost_per_mission()
    return result

@router.get("/aircraft_by_type")
def aircraft_by_type():
    aircraft_service = Aircraftservice()
    method = aircraft_service.aircraft_by_type()
    return method