from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.services.score_service import ScoreCalculator
from app.services.weather_service import Weather
from app.db.entities import AircraftScore
from app.services.distance_service import Route
class RecommendationService:
    def recommendation(self, mission, missionid):
        ranking_list = []
        db = sessionLocal()
        weather_service = Weather()
        airport_service = Route()
        try:
            airport_coords = airport_service.coords_airports(mission)
            weather_score = weather_service.mission_weather_score(
                airport_coords["origin_lat"],
                airport_coords["origin_lon"],
                airport_coords["destination_lat"],
                airport_coords["destination_lon"]
            )
            aircrafts = db.query(Aircraft).all()
            for aircraft in aircrafts:
                calculator = ScoreCalculator(mission, aircraft, weather_score["weather_score"])  
                cost = calculator.cost_score()
                rng = calculator.range_score()
                speed = calculator.speed_score()
                capacity = calculator.capacity_score()
                final = calculator.final_score()

                score = AircraftScore(
                    mission_id=missionid,
                    aircraft_id=aircraft.id,
                    cost_score=cost,
                    range_score=rng,
                    speed_score=speed,
                    capacity_score=capacity,
                    weather_score=weather_score["weather_score"],
                    final_score=final
                )
                db.add(score)
                ranking_list.append({
                    "name": aircraft.name,
                    "cost_score": cost,
                    "range_score": rng,
                    "speed_score": speed,
                    "capacity_score": capacity,
                    "weather_score": weather_score["weather_score"],
                    "avg_wind": weather_score["avg_wind"],
                    "avg_visibility": weather_score["avg_visibility"],
                    "avg_precipitation": weather_score["avg_precipitation"],
                    "avg_temperature": weather_score["avg_temperature"],
                    "final_score": final
                })
            db.commit()
        finally:
            db.close()
            ranking_list.sort(key=lambda x: x["final_score"], reverse=True)

        return ranking_list