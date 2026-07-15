from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.services.score_service import ScoreCalculator
from app.db.entities import AircraftScore

class RecommendationService:
    def recommendation(self, mission, missionid):
        ranking_list = []
        db = sessionLocal()
        try:
            aircrafts = db.query(Aircraft).all()
            for aircraft in aircrafts:
                calculator = ScoreCalculator(mission, aircraft)
                final_score = calculator.final_score()
                score = AircraftScore(
                                    mission_id = missionid,
                                    aircraft_id = aircraft.id,
                                    cost_score = calculator.cost_score(),
                                    range_score = calculator.range_score(),
                                    speed_score = calculator.speed_score(),
                                    capacity_score = calculator.capacity_score(),
                                    final_score = calculator.final_score()
                                    )
                db.add(score)
                ranking_list.append({"name": aircraft.name,
                                     "cost_score" : calculator.cost_score(),
                                     "range_score" : calculator.range_score(),
                                     "speed_score" : calculator.speed_score(),
                                     "capacity_score": calculator.capacity_score(),
                                     "final_score" : final_score})
            db.commit()
        finally:
            db.close()
            ranking_list.sort(key=lambda x: x["final_score"], reverse= True)
   
        return ranking_list