from fastapi import FastAPI, APIRouter
from app.db.entities import Mission
from app.db.database import sessionLocal
from app.schemas.mission_schema import MissionRequest
from app.schemas.mission_schema import MissionResponse
from app.services.recommendation_score import RecommendationService
from app.services.AI.llm_configuration import LLMService
from app.services.mission_service import MissionService
from app.services.distance_service import Route
from app.services.aircraft_service import Aircraftservice
from app.services.flighttime_service import FlightTime
from app.services.cost_service import CostService
from fastapi.responses import HTMLResponse
from typing import List
router = APIRouter(prefix="/recommendation", tags=["Recommendation"])

@router.post("/post_mission")
def recommendation(mission : MissionRequest):
    rota = Route()
    distance = rota.calculate_route_distance(mission)
    mission.distance_km = distance

    mission_service = MissionService()
    new_mission_id = mission_service.create_mission(mission)

    recommendation_service = RecommendationService()
    ranking_list = recommendation_service.recommendation(mission, new_mission_id)
    best_aircraft_json = ranking_list[0]

    aircraftservice = Aircraftservice()
    aircraft = aircraftservice.get_aircraft(best_aircraft_json["name"])

    time_service =FlightTime()
    mission_time = time_service.flight_time(aircraft.cruise_speed, distance)

    cost_service = CostService()
    total_cost = cost_service.total_cost(mission_time, aircraft.operational_cost_hour)

    ai_agent = LLMService()
    response_ai_agent = ai_agent.explain(mission, best_aircraft_json, aircraft)

    mission_service.update_mission(
        new_mission_id,
        best_aircraft=best_aircraft_json["name"],
        final_score=best_aircraft_json["final_score"],
        mission_time=mission_time,
        total_cost=total_cost,
    )

    route_coords = rota.routes_coords(mission)
    origem = route_coords["origem"]
    destino = route_coords["destino"]
    info_dict = {
        "resposta": response_ai_agent,
        "ranking" : ranking_list, 
        "best": best_aircraft_json["name"], 
        "distance": distance,
        "capacity_score": best_aircraft_json["capacity_score"],
        "speed_score": best_aircraft_json["speed_score"],
        "weather_score": best_aircraft_json["weather_score"],
        "avg_wind": best_aircraft_json["avg_wind"],
        "avg_visibility": best_aircraft_json["avg_visibility"],
        "avg_precipitation": best_aircraft_json["avg_precipitation"],    
        "avg_temperature": best_aircraft_json["avg_temperature"],
        "cost_score": best_aircraft_json["cost_score"],
        "range_score": best_aircraft_json["range_score"],
        "final_score": best_aircraft_json["final_score"],
        "mission_time": mission_time,
        "total_cost": total_cost,
        "origem_lat": origem[0],
        "origem_lon":origem[1],
        "destino_lat": destino[0],
        "destino_lon" : destino[1],
        "origin_name": mission.origin_airport,
        "destination_name" : mission.destination_airport,
        "mission_id": new_mission_id
        }
    
    return  info_dict

@router.get("/historic_missions", response_model=List[MissionResponse])
def historic_missions():
    mission_service = MissionService()
    lista = mission_service.historic_missions()
    return lista
