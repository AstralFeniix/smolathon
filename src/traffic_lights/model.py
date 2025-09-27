from pydantic import BaseModel


class TrafficLight(BaseModel):
    id: int | None = None
    address: str
    type: str
    install_year: int