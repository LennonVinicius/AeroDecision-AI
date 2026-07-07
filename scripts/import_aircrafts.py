import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
from app.db.entities import Aircraft
from app.db.database import sessionLocal

with open("aircrafts.json", "r", encoding="utf-8") as f:
    aircrafts = json.load(f)

db = sessionLocal()

for aircraft in aircrafts:
    new = Aircraft(
        name=aircraft["name"],
        manufacturer=aircraft["manufacturer"],
        family = aircraft["family"],
        aircraft_type = aircraft["aircraft_type"],
        range_km=aircraft["range_km"],
        max_passengers=aircraft["max_passengers"],
        max_payload_kg=aircraft["max_payload_kg"],
        cruise_speed=aircraft["cruise_speed"],
        fuel_consumption=aircraft["fuel_consumption"],
        mission_type=aircraft["mission_type"],
        runway_requirement=aircraft["runway_requirement"],
        operational_cost_hour=aircraft["operational_cost_hour"],
        mtow_kg = aircraft["mtow_kg"],
        landing_weight_kg = aircraft["landing_weight_kg"],
        usable_fuel_kg = aircraft["usable_fuel_kg"],
        service_ceiling_ft = aircraft["service_ceiling_ft"],
        engine_model = aircraft["engine_model"],
        engines = aircraft["engines"],
        source = aircraft["source"]
    )
    db.add(new)
db.commit()
db.close()    