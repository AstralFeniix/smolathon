from datetime import date

from fastapi import APIRouter

from . import service, model


router = APIRouter(
    prefix="/services",
    tags=["services"]
)


@router.get("/")
async def get_one_service(name: str) -> model.Service | bool:
    return await service.get_one_service(name)

@router.get("/requests")
async def get_one_service_request(
    service_id: int | None=None,
    customer_name: str | None=None,
    created_at: date | None=None,
    status: model.Status | None=None
) -> model.ServiceRequest | bool:
    return await service.get_one_service_request(service_id, customer_name, created_at, status)

@router.get("/requests/many")
async def get_many_service_requests(
    service_id: int | None=None,
    customer_name: str | None=None,
    created_at: date | None=None,
    status: model.Status | None=None,
    limit: int = 1
) -> list[model.ServiceRequest] | bool:
    return await service.get_many_service_requests(service_id, customer_name, created_at, status, limit)

@router.get("/requests/all")
async def get_all_service_requests() -> list[model.ServiceRequest] | bool:
    return await service.get_all_service_requests()

@router.post("/")
async def post_service(serv: model.Service) -> bool:
    return await service.post_service(serv)

@router.post("/requests")
async def post_service_request(service_request: model.ServiceRequest) -> bool:
    return await service.post_service_request(service_request)