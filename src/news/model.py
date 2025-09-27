from datetime import date

from pydantic import BaseModel


class News(BaseModel):
    id: int | None = None
    title: str
    content: str
    publish_date: date
    image_url: str
    is_published: bool
