from datetime import date

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/")
async def get_one_news(
    id: int | None=None,
    publish_date: date | None=None,
    is_published: bool | None=None,
) -> model.News | bool:
    return await service.get_one_news(id, publish_date, is_published)

@router.get("/many")
async def get_many_news(
    publish_date: date | None=None,
    is_published: bool | None=None,
    limit: int = 1
) -> list[model.News] | bool:
    return await service.get_many_news(publish_date, is_published, limit)

@router.post("/")
async def post_news(news: model.News) -> bool:
    return await service.post_news(news)

@router.patch("/")
async def patch_news(
    id: int,
    title: str,
    content: str,
    is_published: bool
) -> bool:
    return await service.patch_news(id, title, content, is_published)

@router.delete("/")
async def delete_news(
    id: int
) -> bool:
    return await service.delete_news(id)