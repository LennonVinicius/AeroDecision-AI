
from app.db.database import sessionLocal
from app.db.entities import Airport
import csv
import os
db = sessionLocal()
BATCH_SIZE= 1000
inseridos = 0
icaos_vistos = set()
with open("airports.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):
        icao =row["icao_code"].strip() or row["gps_code"].strip()
        if not icao or not row["name"].strip() or len(icao) != 4:
            continue
        if icao in icaos_vistos:     
            continue
        icaos_vistos.add(icao)       
        new = Airport(
            icao = icao,
            iata = row["iata_code"].strip() or None,
            name=row["name"].strip(),
            latitude = float(row["latitude_deg"]),
            longitude = float(row["longitude_deg"]),
            city=row["municipality"].strip() or row["iso_region"],
            country=row["iso_country"],
            runway_length=None,
        )
        db.add(new)
        inseridos+=1
        print(inseridos)
        db.commit()
db.commit()
db.close()