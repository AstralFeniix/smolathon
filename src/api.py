from fastapi import FastAPI

from src.user.controller import router as users_router
from src.accidents.controller import router as accidents_router
from src.news.controller import router as news_router
from src.traffic_lights.controller import router as traffic_lights_router
from src.fines.controller import router as fines_router
from src.services.controller import router as services_router
from src.evacuations.controller import router as evacuations_router

# All routers
routers = (
    users_router,
    accidents_router,
    news_router,
    traffic_lights_router,
    fines_router,
    services_router,
    evacuations_router,
)

# Routers registrations
def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)