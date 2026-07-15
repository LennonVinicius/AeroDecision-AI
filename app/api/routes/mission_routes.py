from fastapi import FastAPI, APIRouter
from app.db.entities import Mission
from app.db.database import sessionLocal
from app.schemas.mission_schema import MissionRequest
from app.services.recommendation_score import RecommendationService
from app.services.AI.llm_configuration import LLMService
from app.services.mission_service import MissionService
from app.services.distance_service import Route
from app.services.aircraft_service import Aircraftservice
router = APIRouter(prefix="/recommendation", tags=["Recommendation"])

@router.post("/post_mission")
def recommendation(mission : MissionRequest):
    rota = Route()
    distance = rota.calculate_route_distance(mission)
    mission.distance_km = distance

    mission_service = MissionService()
    new_mission_id = mission_service.create_mission(mission)

    recommendation_service = RecommendationService()
    json_recommendation = recommendation_service.recommendation(mission, new_mission_id)


    
    best_aircraft_json = json_recommendation[0]

    aircraftservice = Aircraftservice()
    aircraft = aircraftservice.get_aircraft(best_aircraft_json["name"])
    ai_agent = LLMService()
    response_ai_agent = ai_agent.explain(mission, best_aircraft_json, aircraft)

    return {"resposta": response_ai_agent, "best": best_aircraft_json["name"]}

    