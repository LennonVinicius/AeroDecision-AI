import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import json
from app.db.entities import Aircraft
from app.db.database import sessionLocal


db = sessionLocal()

with open("aircrafts.json", "r", encoding="utf-8") as f:
    aircrafts = json.load(f)

for data in aircrafts:

    aircraft = (
        db.query(Aircraft)
        .filter(Aircraft.name == data["name"])
        .first()
    )

    if aircraft:
        aircraft.operational_cost_hour = data["operational_cost_hour"]
        aircraft.range_km = data["range_km"]
        aircraft.max_passengers = data["max_passengers"]
        aircraft.max_payload_kg = data["max_payload_kg"]
        aircraft.cruise_speed = data["cruise_speed"]
        aircraft.mtow_kg = data["mtow_kg"]
        aircraft.usable_fuel_kg = data["usable_fuel_kg"]
        aircraft.service_ceiling_ft = data["service_ceiling_ft"]
        aircraft.runway_requirement = data["runway_requirement"]
        aircraft.landing_weight_kg = data["landing_weight_kg"]
        aircraft.fuel_consumption = data["fuel_consumption"]
        aircraft.source = data["source"]

    else:
        aircraft = Aircraft(**data)
        db.add(aircraft)

db.commit()
db.close()