from datetime import date
from pydantic import BaseModel


class Accident(BaseModel):
    id: int | None = None
    date: date
    incidents_count: int
    injured_count: int
    fatalities_count: int