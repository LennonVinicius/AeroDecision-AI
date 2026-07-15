from app.db.database import sessionLocal
from app.db.entities import Mission

class MissionService:
    def create_mission(self, mission_request):
        db = sessionLocal()
        try:
            mission = Mission(
                origin_airport=mission_request.origin_airport,
                destination_airport=mission_request.destination_airport,
                passengers=mission_request.passengers,
                cargo_weight=mission_request.cargo_weight,
                mission_type = mission_request.mission_type,
                priority = mission_request.mission_type,
                distance_km= mission_request.distance_km
            )
            db.add(mission)
            db.commit()
            db.refresh(mission)
            return mission.id
        finally:
            db.close()
        