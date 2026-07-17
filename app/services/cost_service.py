from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.db.entities import AircraftScore
from app.db.entities import Mission
from sqlalchemy import func
from datetime import datetime

class CostService:
    def total_cost(self, time_mission, cost_per_hour):
        result = time_mission * cost_per_hour
        return result
    
    def cost_per_mission(self):
        today = datetime.now()
        inicio_mes = datetime(today.year, today.month, 1)
        db = sessionLocal()
        try:
            media= db.query(func.avg(Mission.total_cost)).filter(Mission.created_at>=inicio_mes).scalar()
            return media if media is not None else 0
        finally:
            db.close()