import logging
from datetime import date

from fastapi import APIRouter
import psycopg2 as postgres

from .model import News
from src.database import DATABASE_URL


async def post_news(news: News) -> bool:
    news_data = (
        news.title,
        news.content,
        news.publish_date,
        news.image_url,
        news.is_published,
    )

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """INSERT INTO news (title, content, publish_date, image_url, is_published)
                    VALUES (%s, %s, %s, %s, %s);""",
                    news_data
                )
                return True

            except Exception as e:
                logging.error(f"Failed to insert into `news` database: {e}")

    return False

async def get_one_news(
    id: int | None=None,
    publish_date: date | None=None,
    is_published: bool | None=None,
) -> News | bool:
    news = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, title, content, publish_date, image_url, is_published FROM news 
                    WHERE id = %s OR publish_date = %s OR is_published = %s;""",
                    (id, publish_date, is_published)
                )
                news_record = cur.fetchone()

                if news_record:
                    news = News(
                        id=news_record[0],
                        title=news_record[1],
                        content=news_record[2],
                        publish_date=news_record[3],
                        image_url=news_record[4],
                        is_published=news_record[5]
                    )

            except Exception as e:
                logging.error(f"Failed to select (one) from `news` database: {e}")

    return news if news else False

async def get_many_news(
    publish_date: date | None=None,
    is_published: bool | None=None,
    limit: int = 1
) -> list[News] | bool:
    news = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """SELECT id, title, content, publish_date, image_url, is_published FROM news 
                    WHERE publish_date = %s OR is_published = %s;""",
                    (publish_date, is_published)
                )
                news_records = cur.fetchmany(limit)

                if news_records:
                    news = list(
                        map(
                            lambda news: News(
                                    id=news[0],
                                    title=news[1],
                                    content=news[2],
                                    publish_date=news[3],
                                    image_url=news[4],
                                    is_published=news[5]
                            ), news_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `news` database: {e}")

    return news if news else False

async def get_all_news() -> list[News] | bool:
    news = None

    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM news"
                )
                news_records = cur.fetchall()

                if news_records:
                    news = list(
                        map(
                            lambda news: News(
                                    id=news[0],
                                    title=news[1],
                                    content=news[2],
                                    publish_date=news[3],
                                    image_url=news[4],
                                    is_published=news[5]
                            ), news_records
                        )
                    )

            except Exception as e:
                logging.error(f"Failed to select (many) from `news` database: {e}")

    return news if news else False

async def patch_news(
    id: int,
    title: str,
    content: str,
    is_published: bool
) -> bool:
    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    """UPDATE news SET title = %s, content = %s, is_published = %s
                    WHERE id = %s;""",
                    (title, content, is_published, id)
                )
                return True

            except Exception as e:
                logging.error(f"Failed to update `news` database: {e}")

    return False

async def delete_news(
    id: int
) -> bool:
    with postgres.connect(DATABASE_URL) as connection:
        with connection.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM news WHERE id = %s;",
                    (id,)
                )
                return True

            except Exception as e:
                logging.error(f"Failed to delete row in `news` database: {e}")

    return False