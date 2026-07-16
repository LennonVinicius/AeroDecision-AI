from app.db.database import sessionLocal
from app.db.entities import Mission
from datetime import datetime
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

    def update_mission(self, mission_id, **kwargs):
        db = sessionLocal()
        try:
            mission = db.query(Mission).filter(Mission.id == mission_id).first()
            if not mission:
                return None
            for campo, valor in kwargs.items():
                setattr(mission, campo, valor)

            db.commit()
            db.refresh(mission)
            return mission 
        finally:
            db.close()

    def get_mission_month(self):      
        db = sessionLocal()
        try:
            today = datetime.now()
            inicio_mes = datetime(today.year, today.month, 1)
            lista = db.query(Mission).filter(Mission.created_at >= inicio_mes).all()
            return len(lista)
        finally:
            db.close()

    def historic_missions(self):
        db = sessionLocal()
        try:
            today = datetime.now()
            inicio_mes = datetime(today.year, today.month, 1)
            lista = db.query(Mission).filter(Mission.created_at >= inicio_mes).all()
            return lista    
        finally:
            db.close()
