from datetime import date

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/evacuations",
    tags=["evacuations"]
)


@router.get("/")
async def get_one_evacuation(date: date) -> model.Evacuation | bool:
    return await service.get_one_evacuation(date)

@router.get("/routes")
async def get_one_evacuation_route(
    year: int | None=None,
    month: str | None=None,
    route: str | None=None,
) -> model.EvacuationRoute | bool:
    return await service.get_one_evacuation_route(year, month, route)

@router.get("/many")
async def get_many_evacuations(
    date: date,
    limit: int = 1
) -> list[model.Evacuation] | bool:
    return await service.get_many_evacuations(date, limit)

@router.get("/routes/many")
async def get_many_evacuation_routes(
    year: int | None=None,
    month: str | None=None,
    route: str | None=None,
    limit: int = 1
) -> list[model.EvacuationRoute] | bool:
    return await service.get_many_evacuation_routes(year, month, route)

@router.get("/all")
async def get_all_evacuations() -> list[model.Evacuation] | bool:
    return await service.get_all_evacuations()

@router.get("/routes/all")
async def get_all_evacuation_routes() -> list[model.EvacuationRoute] | bool:
    return await service.get_all_evacuation_routes()

@router.post("/")
async def post_evacuation(evacuation: model.Evacuation) -> bool:
    return await service.post_evacuation(evacuation)

@router.post("/requests")
async def post_evacuation_route(evacuation_route: model.EvacuationRoute) -> bool:
    return await service.post_evacuation_route(evacuation_route)
