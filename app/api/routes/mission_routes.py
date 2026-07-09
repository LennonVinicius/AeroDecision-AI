from fastapi import FastAPI, APIRouter
from app.db.entities import Mission
from db.database import sessionLocal
from app.schemas.mission_schema import MissionRequest
from app.services.recommendation_score import RecommendationService
from services.AI.llm_configuration import LLMService
router = APIRouter(prefix="/recommendation", tags=["Recommendation"])

@router.post("/")
def recommendation(mission : MissionRequest):
    new_mission = Mission(
        origin_airport=mission.origin_airport,
        destination_airport=mission.destination_airport,
        passengers=mission.passengers,
        cargo_weight=mission.cargo_weight,
        priority=mission.priority
    )
    try:
        db = sessionLocal()
        db.add(new_mission)
        db.commit()
        db.refresh(new_mission)
    finally:
        db.close()
    service = RecommendationService()
    json_recommendation = service.recommendation(new_mission)
    ai_agent = LLMService()
    best_aircraft = json_recommendation[0]
    response_ai_agent = ai_agent.explain(new_mission, best_aircraft[0])

    return response_ai_agent

    