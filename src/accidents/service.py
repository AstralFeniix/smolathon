import logging
import datetime

from fastapi import APIRouter
import psycopg2 as postgres

from .model import Accident
from src.database import DATABASE_URL


async def post_accident(accident: Accident) -> bool:
    accident_data = (
        accident.date,
        accident.incidents_count,
        accident.injured_count,
        accident.fatalities_count,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO accidents (date, incidents_count, injured_count, fatalities_count) 
                    VALUES (%s, %s, %s, %s);
                    """,
                    accident_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `accidents` database: {e}") 

    return False


async def get_one_accident(
    id: int | None=None,
    date: datetime.date | None=None
) -> Accident | bool:
    accident = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, incidents_count, injured_count, fatalities_count FROM accidents 
                    WHERE id = %s OR date = %s;""",
                    (id, date)
                )
                accident_record = cur.fetchone()

                if accident_record:
                    accident = Accident(
                        id=accident_record[0],
                        date=accident_record[1],
                        incidents_count=accident_record[2],
                        injured_count=accident_record[3],
                        fatalities_count=accident_record[4],
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `accidents` database: {e}")

    return accident if accident else False

async def get_many_accidents(
    date: datetime.date | None=None,
    limit: int = 1
) -> list[Accident] | bool:
    accidents = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, incidents_count, injured_count, fatalities_count FROM accidents 
                    WHERE date = %s""",
                    (date, )
                )
                accident_records = cur.fetchmany(limit)

                if accident_records:
                    accidents = list(
                        map(
                            lambda accident: Accident(
                                    id=accident[0],
                                    date=accident[1],
                                    incidents_count=accident[2],
                                    injured_count=accident[3],
                                    fatalities_count=accident[4],
                            ), accident_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `accidents` database: {e}")

    return accidents if accidents else False
