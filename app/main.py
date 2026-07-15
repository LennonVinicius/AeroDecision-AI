from fastapi import FastAPI
from app.api.routes.mission_routes import router as recommendation_router
from app.api.routes.fleet_routes import router as aircraft_router
from app.api.routes.airport_routes import router as airport_router

app = FastAPI(
    title="AeroDecision AI",
    version="1.0.0"
)

app.include_router(recommendation_router)
app.include_router(aircraft_router)
app.include_router(airport_router)