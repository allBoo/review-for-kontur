from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, field_validator, Field, PrivateAttr
from typing import Literal, Any


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
    timestamp: datetime
    _sent_timestamp: datetime = PrivateAttr(default_factory=lambda: datetime.now(timezone.utc))
    meta: DeviceMeta

    @property
    def sent_timestamp(self) -> datetime:
        return self._sent_timestamp

    @field_validator('timestamp')
    @classmethod
    def timestamp_add_tz(cls, timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        return timestamp

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        model_dict = super().model_dump(*args, **kwargs)
        model_dict["sent_timestamp"] = self._sent_timestamp

        return model_dict


class EventType(Enum):
    PLAY = "play"
    ERROR = "error"
    PING = "ping"


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


class PlayMeta(BaseModel):
    startTime: datetime
    duration: float


class ErrorMeta(BaseModel):
    code: str
    message: str | None = None


class EventRequest(Event):
    """
    Base Event
    Contains device and content metadata
    """
    class Config:
        abstract = True

    content: ContentMeta
    playlist: PlaylistMeta


# final
class PingRequest(Event):
    """
    Ping Request
    contains only device metadata
    """
    type: Literal['ping']


# final
class PlayEventRequest(EventRequest):
    """
    Play Event
    Contains device, content metadata and play metadata
    """
    type: Literal['play']
    play: PlayMeta


# final
class ErrorEventRequest(EventRequest):
    """
    Error Event
    Contains device, content metadata and error
    """
    type: Literal['error']
    error: ErrorMeta
