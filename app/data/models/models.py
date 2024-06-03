from pydantic import BaseModel
from datetime import datetime


class Device(BaseModel):
    id: int
    udid: str
    account_id: int
    location_id: int


class Event(BaseModel):
    id: int
    device_id: int
    type: str
    content_id: int
    timestamp: datetime

