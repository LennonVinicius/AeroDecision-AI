from app.db.entities import Mission, Aircraft
MAX_CRUISE = 870
MAX_COST = 11500
class ScoreCalculator():
    def __init__(self, mission : Mission, aircraft : Aircraft):
        self.aircraft = aircraft
        self.mission = mission

    def range_score(self):
        score = (self.aircraft.range_km * 100) / self.mission.distance_km
        return score
    
    def capacity_score(self):
        score = (self.aircraft.max_passengers * 100) / self.mission.passengers
        return score
    
    def payload_score(self):
        score = (self.aircraft.max_payload_kg *100)/ self.mission.cargo_volume
        return score
    def speed_score(self):
        score = (self.aircraft.cruise_speed / MAX_CRUISE) * 100
        return score
    def cost_score(self):
        return (1 - (self.aircraft.operational_cost_hour / MAX_COST)) * 100
    def final_score(self):
        final = self.range_score() *0.30 + self.capacity_score() *0.25 + self.payload_score() *0.20 +self.speed_score() *0.15 + self.cost_score() * 0.10
        return final