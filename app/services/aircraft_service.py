from app.db.database import sessionLocal
from app.db.entities import Aircraft
from app.db.entities import AircraftScore
from app.db.entities import Mission
from sqlalchemy import func
class Aircraftservice:
    def get_aircraft(self, aircraft_name):
        db = sessionLocal()
        try:
            aircraft = db.query(Aircraft).filter(Aircraft.name == aircraft_name).first()
            return aircraft
        finally:
            db.close()
            
    def get_fleet(self):
        db = sessionLocal()
        try:
            aircraft_list = db.query(Aircraft).all()
            return aircraft_list
        finally:
            db.close()
            
    def most_used_aircraft(self):
        db = sessionLocal()
        try:
            subquery = (
                db.query(AircraftScore.mission_id, func.max(AircraftScore.final_score).label("max_score")).group_by(AircraftScore.mission_id).subquery()
            )
            resultado = (
                        db.query(Aircraft.name, func.count(AircraftScore.id).label("total"))
                        .join(subquery, (AircraftScore.mission_id == subquery.c.mission_id) &
                                        (AircraftScore.final_score == subquery.c.max_score))
                        .join(Aircraft, Aircraft.id == AircraftScore.aircraft_id)
                        .group_by(Aircraft.name)
                        .order_by(func.count(AircraftScore.id).desc())
                        .first()
                    )

            return {"aircraft": resultado[0], "total": resultado[1]} if resultado else {"aircraft": None, "total": 0}
        finally:
            db.close

    def aircraft_by_type(self):
        db = sessionLocal()
        try:
            resultado = (
                db.query(Aircraft.aircraft_type, func.count(Mission.id).label("total"))
                .join(Aircraft, Aircraft.name == Mission.best_aircraft)
                .filter(Mission.best_aircraft.isnot(None))
                .group_by(Aircraft.aircraft_type)
                .all()
            )
            return [{"aircraft_type": tipo, "total": total} for tipo, total in resultado]
        finally:
            db.close()

