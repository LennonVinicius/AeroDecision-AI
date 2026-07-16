from app.db.entities import Mission, Aircraft
MAX_CRUISE = 870
MAX_COST = 11500

class ScoreCalculator():
    def __init__(self, mission : Mission, aircraft : Aircraft):
        self.aircraft = aircraft
        self.mission = mission
        
    def range_score(self):
        if self.mission.distance_km == 0:
            return 100
        score = (self.aircraft.range_km * 100) / self.mission.distance_km
        return min(score, 100)
    
    def capacity_score(self):
        score = (self.aircraft.max_passengers * 100) / self.mission.passengers
        return min(score, 100)
    
    def payload_score(self):
        if self.mission.cargo_weight == 0:
            return 100
        score = (self.aircraft.max_payload_kg * 100 ) / self.mission.cargo_weight
        return min(score, 100)
    def speed_score(self):
        score = (self.aircraft.cruise_speed / MAX_CRUISE) * 100
        return min(score, 100)
    def cost_score(self):
        score = (1 - (self.aircraft.operational_cost_hour / MAX_COST)) * 100
        return max(score, 0)
    def final_score(self):
        if not self.is_feasible():
            return 0
        final = self.range_score() *0.30 + self.capacity_score() *0.25 + self.payload_score() *0.20 +self.speed_score() *0.15 + self.cost_score() * 0.10
        return final
    def is_feasible(self):
        return (
            self.aircraft.range_km >= self.mission.distance_km and
            self.aircraft.max_passengers >= self.mission.passengers and
            self.aircraft.max_payload_kg >= self.mission.cargo_weight
        )
