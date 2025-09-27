import datetime

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/accidents",
    tags=["accidents"]
)

@router.get("/")
async def get_one_accident(
    id: int | None=None,
    date: datetime.date | None=None
) -> model.Accident | bool:
    return await service.get_one_accident(id, date)

@router.get("/many")
async def get_many_accidents(
    date: datetime.date | None=None,
    limit: int = 1
) -> list[model.Accident] | bool:
    return await service.get_many_accidents(date, limit)

@router.post("/")
async def post_accident(accident: model.Accident) -> bool:
    return await service.post_accident(accident)
