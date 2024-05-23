from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DeviceMeta(BaseModel):
    """
    Device Metadata
    """
    udid: str
    app: str
    version: str
    env: str


class Event(BaseModel):
    """
    Base Event class
    """
    class Config:
        abstract = True

    type: str
    meta: DeviceMeta


class PingRequest(Event):
    """
    Ping Request
    contains only device metadata
    """
    type: str = "ping"


class EventType(Enum):
    PLAY = "play"
    ERROR = "error"


class ContentType(Enum):
    AD = "ad"
    CUSTOM_AD = "custom-ad"
    CONTENT = "content"


class ContentMeta(BaseModel):
    id: int
    type: ContentType


class PlaylistMeta(BaseModel):
    id: int
    instanceId: int


class ErrorMeta(BaseModel):
    code: str
    message: str | None = None


class EventRequest(Event):
    """
    Play Event
    Contains device and content metadata and optional error
    """
    class Config:
        abstract = True

    type: EventType

    content: ContentMeta
    playlist: PlaylistMeta
    error: ErrorMeta | None = None

    timestamp: datetime
    startTime: datetime | None = None
    duration: float

