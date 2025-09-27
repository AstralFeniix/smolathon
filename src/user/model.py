from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    Editor = "editor"
    Administrator = "admin"

class User(BaseModel):
    id: int | None = None
    name: str
    password: str
    role: Role
