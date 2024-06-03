from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    OK = "ok"
    ERROR = "error"


class EventsResponse(BaseModel):
    status: Status
    message: str | None = None
