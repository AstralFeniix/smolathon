import datetime

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/fines",
    tags=["fines"]
)

@router.get("/")
async def get_one_fine(
    id: int | None=None,
    date: datetime.date | None=None
) -> model.Fine | bool:
    return await service.get_one_fine(id, date)

@router.get("/many")
async def get_many_fines(
    date: datetime.date | None=None,
    limit: int = 1
) -> list[model.Fine] | bool:
    return await service.get_many_fines(date, limit)

@router.get("/all")
async def get_many_fines() -> list[model.Fine] | bool:
    return await service.get_all_fines()

@router.post("/")
async def post_fine(fine: model.Fine) -> bool:
    return await service.post_fine(fine)
