from app.db.database import sessionLocal
from app.db.entities import Aircraft
class Aircraftservice:
    def get_aircraft(self, aircraft_name):
        db = sessionLocal()
        try:
            aircraft = db.query(Aircraft).filter(Aircraft.name == aircraft_name).first()
            return aircraft
        finally:
            db.close()
        
