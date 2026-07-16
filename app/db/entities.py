from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Aircraft(Base):
    __tablename__ = "aircrafts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    family = Column(String)
    aircraft_type = Column(String)
    range_km = Column(Float)
    max_passengers = Column(Integer)
    max_payload_kg = Column(Float)
    cruise_speed= Column(Float)
    runway_requirement = Column(Float)
    landing_weight_kg= Column(Float)
    fuel_consumption= Column(Float)
    mission_type = Column(String)
    operational_cost_hour = Column(Float)
    mtow_kg = Column(Float)
    usable_fuel_kg = Column(Float)
    service_ceiling_ft = Column(Integer)
    engine_model = Column(String)
    engines = Column(Integer)
    source = Column(String)


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    icao = Column(String, unique=True, nullable=True, index=True)
    iata = Column(String, nullable=True)
    name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    runway_length = Column(Float, nullable=True)

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    origin_airport = Column(String, ForeignKey("airports.icao"), nullable=False)
    destination_airport = Column(String, ForeignKey("airports.icao"), nullable=False)
    mission_type = Column(String, nullable=False)
    passengers = Column(Integer, default=0)
    cargo_weight = Column(Float, default=0)
    priority = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    distance_km = Column(Float)
    weather_condition = Column(String)
    required_runway = Column(Float)
    best_aircraft = Column(String, nullable=True)
    final_score = Column(Float, nullable=True)
    mission_time = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)

class AircraftScore(Base):
    __tablename__ = "aircraft_scores"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"), nullable=False)
    cost_score = Column(Float, nullable=False)
    range_score = Column(Float, nullable=False)
    speed_score = Column(Float, nullable=False)
    capacity_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=False)

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    recommended_aircraft = Column(String, nullable=False)
    llm_explanation = Column(String, nullable=False)
    risk_analysis = Column(String, nullable=True)
    operational_notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())