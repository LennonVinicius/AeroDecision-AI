from geopy.distance import geodesic
from app.db.entities import Airport
from app.db.database import sessionLocal

class Route:
    def calculate_route_distance(self, mission) -> float:
        db = sessionLocal()
        try:
            origin_airport = db.query(Airport).filter(Airport.icao == mission.origin_airport).first()
            destination_airport = db.query(Airport).filter(Airport.icao == mission.destination_airport).first()
        finally:
            db.close()
        origem = (origin_airport.latitude, origin_airport.longitude)
        destino = (destination_airport.latitude, destination_airport.longitude)
        return geodesic(origem, destino).km
    def routes_coords(self, mission):
        db = sessionLocal()
        try:
            origin_airport = db.query(Airport).filter(Airport.icao == mission.origin_airport).first()
            destination_airport = db.query(Airport).filter(Airport.icao == mission.destination_airport).first()
        finally:
            db.close()
        origem = [origin_airport.latitude, origin_airport.longitude]
        destino = [destination_airport.latitude, destination_airport.longitude]

        return {"origem": origem, "destino": destino}
