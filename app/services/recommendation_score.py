from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.services.score_service import ScoreCalculator
class RecommendationService:
    def recommendation(self, mission):
        ranking_list = []
        db = sessionLocal()
        try:
            aircrafts = db.query(Aircraft).all()
        finally:
            db.close()
        for aircraft in aircrafts:
            calculator = ScoreCalculator(aircraft, mission)
            final_score = calculator.final_score()
            ranking_list.append({"name": aircraft.name, "final_score" : final_score})
        ranking_list.sort(key=lambda x: x["final_score"], reverse= True)
        return ranking_list