import datetime

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/traffic_lights",
    tags=["traffic_lights"]
)

@router.get("/")
async def get_one_traffic_light(
    id: int | None=None,
    address: str | None=None,
    type: str | None=None,
    install_year: int | None=None
) -> model.TrafficLight | bool:
    return await service.get_one_traffic_light(id, address, type, install_year)

@router.get("/many")
async def get_many_traffic_lights(
    address: str | None=None,
    type: str | None=None,
    install_year: int | None=None,
    limit: int = 1
) -> list[model.TrafficLight] | bool:
    return await service.get_many_traffic_lights(address, type, install_year, limit)

@router.post("/")
async def post_traffic_light(traffic_light: model.TrafficLight) -> bool:
    return await service.post_traffic_light(traffic_light)
