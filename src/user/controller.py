from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def get_user(name: str, password: str) -> model.User | bool:
    return await service.get_user(name, password)

@router.post("/")
async def post_user(user: model.User) -> bool:
    return await service.post_user(user)
