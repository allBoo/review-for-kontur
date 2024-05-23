from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    OK = "OK"
    ERROR = "ERROR"


class EventsResponse(BaseModel):
    status: Status
    message: str | None = None
