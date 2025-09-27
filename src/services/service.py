import logging
from datetime import date

from fastapi import APIRouter
import psycopg2 as postgres

from .model import Service, ServiceRequest, Status
from src.database import DATABASE_URL


async def post_service(service: Service) -> bool:
    service_data = (
        service.name,
        service.descriprion,
        service.price,
        service.is_free,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO services (name, descriprion, price, is_free) 
                    VALUES (%s, %s, %s, %s);
                    """,
                    service_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `services` database: {e}") 

    return False

async def post_service_request(service_request: ServiceRequest) -> bool:
    service_request_data = (
        service_request.service_id,
        service_request.customer_name,
        service_request.phone,
        service_request.address,
        service_request.car_type,
        service_request.created_at,
        service_request.status
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO service_requests (service_id, customer_name, phone, address, car_type, created_at, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    service_request_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `service_requests` database: {e}") 

    return False

async def get_one_service(name: str) -> Service | bool:
    service = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, name, descriprion, price, is_free FROM services 
                    WHERE name = %s;""",
                    (name,)
                )
                service_record = cur.fetchone()

                if service_record:
                    service = Service(
                        id=service_record[0],
                        name=service_record[1],
                        descriprion=service_record[2],
                        price=service_record[3],
                        is_free=service_record[4],
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `services` database: {e}")

    return service if service else False

async def get_one_service_request(
    service_id: int | None=None,
    customer_name: str | None=None,
    created_at: date | None=None,
    status: Status | None=None
) -> ServiceRequest | bool:
    service_request = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, service_id, customer_name, phone, address, car_type, created_at, status FROM service_requests 
                    WHERE service_id = %s OR customer_name = %s OR created_at = %s OR status = %s;""",
                    (service_id, customer_name, created_at, status)
                )
                service_request_record = cur.fetchone()

                if service_request_record:
                    service_request = ServiceRequest(
                        id=service_request_record[0],
                        service_id=service_request_record[1],
                        customer_name=service_request_record[2],
                        phone=service_request_record[3],
                        address=service_request_record[4],
                        car_type=service_request_record[5],
                        created_at=service_request_record[6],
                        status=service_request_record[7]
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `service_requests` database: {e}")

    return service_request if service_request else False

async def get_many_service_requests(
    service_id: int | None=None,
    customer_name: str | None=None,
    created_at: date | None=None,
    status: Status | None=None,
    limit: int = 1
) -> list[ServiceRequest] | bool:
    service_requests = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, service_id, customer_name, phone, address, car_type, created_at, status FROM service_requests 
                    WHERE service_id = %s OR customer_name = %s OR created_at = %s OR status = %s;""",
                    (service_id, customer_name, created_at, status)
                )
                service_request_records = cur.fetchmany(limit)

                if service_request_records:
                    service_requests = list(
                        map(
                            lambda service_request: ServiceRequest(
                                id=service_request[0],
                                service_id=service_request[1],
                                customer_name=service_request[2],
                                phone=service_request[3],
                                address=service_request[4],
                                car_type=service_request[5],
                                created_at=service_request[6],
                                status=service_request[7]
                            ), service_request_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `service_requests` database: {e}")

    return service_requests if service_requests else False

async def get_all_service_requests(
    service_id: int | None=None,
    customer_name: str | None=None,
    created_at: date | None=None,
    status: Status | None=None,
    limit: int = 1
) -> list[ServiceRequest] | bool:
    service_requests = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM service_requests",
                )
                service_request_records = cur.fetchall()

                if service_request_records:
                    service_requests = list(
                        map(
                            lambda service_request: ServiceRequest(
                                id=service_request[0],
                                service_id=service_request[1],
                                customer_name=service_request[2],
                                phone=service_request[3],
                                address=service_request[4],
                                car_type=service_request[5],
                                created_at=service_request[6],
                                status=service_request[7]
                            ), service_request_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (all) from `service_requests` database: {e}")

    return service_requests if service_requests else False
