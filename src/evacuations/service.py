import logging
from datetime import date

from fastapi import APIRouter
import psycopg2 as postgres

from .model import Evacuation, EvacuationRoute
from src.database import DATABASE_URL


async def post_evacuation(evacuation: Evacuation) -> bool:
    evacuation_data = (
        evacuation.date,
        evacuation.evacuator_count,
        evacuation.trips_count,
        evacuation.evacuations_count,
        evacuation.parking_fine_sum,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO evacuations (date, evacuators_count, trips_count, evacuations_count, parking_fine_sum) 
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    evacuation_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `evacuations` database: {e}") 

    return False

async def post_evacuation_route(evacuation_route: EvacuationRoute) -> bool:
    evacuation_route_data = (
        evacuation_route.year,
        evacuation_route.month,
        evacuation_route.route,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO evacuations_routes (year, month, route) 
                    VALUES (%s, %s, %s);
                    """,
                    evacuation_route_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `evacuations_routes` database: {e}") 

    return False

async def get_one_evacuation(date: date) -> Evacuation | bool:
    evacuation = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, evacuators_count, trips_count, evacuations_count, parking_fine_sum FROM evacuations 
                    WHERE date = %s;""",
                    (date,)
                )
                evacuation_record = cur.fetchone()

                if evacuation_record:
                    evacuation = Evacuation(
                        id=evacuation_record[0],
                        date=evacuation_record[1],
                        evacuator_count=evacuation_record[2],
                        trips_count=evacuation_record[3],
                        evacuations_count=evacuation_record[4],
                        parking_fine_sum=evacuation_record[5]
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `evacuations` database: {e}")

    return evacuation if evacuation else False

async def get_one_evacuation_route(
    year: int | None=None,
    month: str | None=None,
    route: str | None=None,
) -> EvacuationRoute | bool:
    evacuation_route = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, year, month, route FROM evacuations_routes 
                    WHERE year = %s OR month = %s OR route = %s;""",
                    (year, month, route)
                )
                evacuation_route_record = cur.fetchone()

                if evacuation_route_record:
                    evacuation_route = EvacuationRoute(
                        id=evacuation_route_record[0],
                        year=evacuation_route_record[1],
                        month=evacuation_route_record[2],
                        route=evacuation_route_record[3],
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `evacuations_routes` database: {e}")

    return evacuation_route if evacuation_route else False

async def get_many_evacuations(
    date: date,
    limit: int = 1
) -> list[Evacuation] | bool:
    evacuations = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, evacuators_count, trips_count, evacuations_count, parking_fine_sum FROM evacuations 
                    WHERE date = %s;""",
                    (date,)
                )
                evacuation_records = cur.fetchmany(limit)

                if evacuation_records:
                    evacuations = list(
                        map(
                            lambda evacuation: Evacuation(
                                id=evacuation[0],
                                date=evacuation[1],
                                evacuator_count=evacuation[2],
                                trips_count=evacuation[3],
                                evacuations_count=evacuation[4],
                                parking_fine_sum=evacuation[5]
                            ), evacuation_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `evacuations` database: {e}")

    return evacuations if evacuations else False

async def get_many_evacuation_routes(
    year: int | None=None,
    month: str | None=None,
    route: str | None=None,
    limit: int = 1
) -> list[EvacuationRoute] | bool:
    evacuation_routes = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, year, month, route FROM evacuations_routes
                    WHERE year = %s OR month = %s OR route = %s;""",
                    (year, month, route)
                )
                evacuation_route_records = cur.fetchmany(limit)

                if evacuation_route_records:
                    evacuation_routes = list(
                        map(
                            lambda evacuation_route: EvacuationRoute(
                                id=evacuation_route[0],
                                year=evacuation_route[1],
                                month=evacuation_route[2],
                                route=evacuation_route[3],
                            ), evacuation_route_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `evacuations_routes` database: {e}")

    return evacuation_routes if evacuation_routes else False

async def get_all_evacuations() -> list[Evacuation] | bool:
    evacuations = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM evacuations;",
                )
                evacuation_records = cur.fetchall()

                if evacuation_records:
                    evacuations = list(
                        map(
                            lambda evacuation: Evacuation(
                                id=evacuation[0],
                                date=evacuation[1],
                                evacuator_count=evacuation[2],
                                trips_count=evacuation[3],
                                evacuations_count=evacuation[4],
                                parking_fine_sum=evacuation[5]
                            ), evacuation_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (all) from `evacuations` database: {e}")

    return evacuations if evacuations else False

async def get_all_evacuation_routes() -> list[EvacuationRoute] | bool:
    evacuation_routes = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM evacuations_routes;"
                )
                evacuation_route_records = cur.fetchall()

                if evacuation_route_records:
                    evacuation_routes = list(
                        map(
                            lambda evacuation_route: EvacuationRoute(
                                id=evacuation_route[0],
                                year=evacuation_route[1],
                                month=evacuation_route[2],
                                route=evacuation_route[3],
                            ), evacuation_route_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (all) from `evacuations_routes` database: {e}")

    return evacuation_routes if evacuation_routes else False
