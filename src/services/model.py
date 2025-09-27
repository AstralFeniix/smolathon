from enum import Enum
from datetime import date

from pydantic import BaseModel


class Status(str, Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"

class Service(BaseModel):
    id: int | None = None
    name: str
    descriprion: str
    price: float
    is_free: bool

class ServiceRequest(BaseModel):
    id: int | None = None
    service_id: int
    customer_name: str
    phone: str
    address: str
    car_type: str
    created_at: date
    status: Status
