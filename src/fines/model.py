from datetime import date

from pydantic import BaseModel


class Fine(BaseModel):
    id: int | None = None
    date: date
    violations_count: int
    decrees_count: int
    fines_issued_sum: float
    fines_collected_sum: float