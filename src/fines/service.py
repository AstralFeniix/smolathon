import logging
import datetime

from fastapi import APIRouter
import psycopg2 as postgres

from .model import Fine
from src.database import DATABASE_URL


async def post_fine(fine: Fine) -> bool:
    fine_data = (
        fine.date,
        fine.violations_count,
        fine.decrees_count,
        fine.fines_issued_sum,
        fine.fines_collected_sum,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO fines (date, violations_count, decrees_count, fines_issued_sum, fines_collected_sum) 
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    fine_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `fines` database: {e}") 

    return False


async def get_one_fine(
    id: int | None=None,
    date: datetime.date | None=None
) -> Fine | bool:
    fine = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, violations_count, decrees_count, fines_issued_sum, fines_collected_sum FROM fines 
                    WHERE id = %s OR date = %s;""",
                    (id, date)
                )
                fine_record = cur.fetchone()

                if fine_record:
                    fine = Fine(
                        id=fine_record[0],
                        date=fine_record[1],
                        violations_count=fine_record[2],
                        decrees_count=fine_record[3],
                        fines_issued_sum=fine_record[4],
                        fines_collected_sum=fine_record[5]
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `fines` database: {e}")

    return fine if fine else False

async def get_many_fines(
    date: datetime.date | None=None,
    limit: int = 1
) -> list[Fine] | bool:
    fines = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, date, violations_count, decrees_count, fines_issued_sum, fines_collected_sum FROM fines 
                    WHERE date = %s;""",
                    (date, )
                )
                fines_records = cur.fetchmany(limit)

                if fines_records:
                    fines = list(
                        map(
                            lambda fine: Fine(
                                id=fine[0],
                                date=fine[1],
                                violations_count=fine[2],
                                decrees_count=fine[3],
                                fines_issued_sum=fine[4],
                                fines_collected_sum=fine[5]
                            ), fines_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `fines` database: {e}")

    return fines if fines else False


async def get_all_fines() -> list[Fine] | bool:
    fines = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM fines;"
                )
                fines_records = cur.fetchall()

                if fines_records:
                    fines = list(
                        map(
                            lambda fine: Fine(
                                id=fine[0],
                                date=fine[1],
                                violations_count=fine[2],
                                decrees_count=fine[3],
                                fines_issued_sum=fine[4],
                                fines_collected_sum=fine[5]
                            ), fines_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (all) from `fines` database: {e}")

    return fines if fines else False