import logging

from fastapi import APIRouter
import psycopg2 as postgres

from .model import TrafficLight
from src.database import DATABASE_URL


async def post_traffic_light(traffic_light: TrafficLight) -> bool:
    traffic_light_data = (
        traffic_light.address,
        traffic_light.type,
        traffic_light.install_year,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO traffic_lights (address, type, install_year) VALUES (%s, %s, %s);",
                    traffic_light_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `traffic_lights` database: {e}")

    return False

async def get_one_traffic_light(
    id: int | None=None,
    address: str | None=None,
    type: str | None=None,
    install_year: int | None=None
) -> TrafficLight | bool:
    traffic_light = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, address, type, install_year FROM traffic_lights 
                    WHERE id = %s OR address = %s OR type = %s OR install_year = %s;""",
                    (id, address, type, install_year)
                )
                traffic_light_record = cur.fetchone()

                if traffic_light_record:
                    traffic_light = TrafficLight(
                        id=traffic_light_record[0],
                        address=traffic_light_record[1],
                        type=traffic_light_record[2],
                        install_year=traffic_light_record[3],
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `traffic_lights` database: {e}")

    return traffic_light if traffic_light else False

async def get_many_traffic_lights(
    address: str | None=None,
    type: str | None=None,
    install_year: int | None=None,
    limit: int = 1
) -> list[TrafficLight] | bool:
    traffic_lights = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, address, type, install_year FROM traffic_lights 
                    WHERE address = %s OR type = %s OR install_year = %s;""",
                    (address, type, install_year)
                )
                traffic_light_records = cur.fetchmany(limit)

                if traffic_light_records:
                    traffic_lights = list(
                        map(
                            lambda traffic_light: TrafficLight(
                                    id=traffic_light[0],
                                    address=traffic_light[1],
                                    type=traffic_light[2],
                                    install_year=traffic_light[3],
                            ), traffic_light_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `traffic_lights` database: {e}")

    return traffic_lights if traffic_lights else False
