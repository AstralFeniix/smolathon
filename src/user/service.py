import logging

from fastapi import APIRouter
import psycopg2 as postgres

from .model import User
from src.database import DATABASE_URL


async def post_user(user: User) -> bool:
    user_data = (
        user.name,
        user.password,
        user.role,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO users (name, password, role) VALUES (%s, %s, %s);",
                    user_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `users` database: {e}")

    return False

async def get_user(name: str, password: str) -> User | bool:
    user = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT id, name, password, role FROM users WHERE name = %s AND password = %s",
                    (name, password)
                )
                user_record = cur.fetchone()

                if user_record:
                    user = User(
                        id=user_record[0],
                        name=user_record[1],
                        password=user_record[2],
                        role=user_record[3],
                    )

            except Exception as e:
                logging.error(f"Failed to select from `users` database: {e}")

    return user if user else False

async def delete_user(
    id: int
) -> bool:
    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM users WHERE id = %s;",
                    (id,)
                )
                return True

            except Exception as e:
                logging.error(f"Failed to delete row in `news` database: {e}")

    return False