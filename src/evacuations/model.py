from datetime import date

from pydantic import BaseModel


class Evacuation(BaseModel):
    id: int | None=None
    date: date
    evacuator_count: int
    trips_count: int
    evacuations_count: int
    parking_fine_sum: float

class EvacuationRoute(BaseModel):
    id: int | None=None
    year: int
    month: str
    route: str
