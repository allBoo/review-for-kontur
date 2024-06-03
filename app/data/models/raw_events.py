from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, PrivateAttr, field_validator
from datetime import datetime, timezone


class EventType(Enum):
    PLAY = "play"
    ERROR = "error"
    PING = "ping"


class ContentType(Enum):
    AD = "ad"
    CUSTOM_AD = "custom-ad"
    CONTENT = "content"


class DeviceMeta(BaseModel):
    """
    Device Metadata
    """
    udid: str
    app: str
    version: str
    env: str


class ContentMeta(BaseModel):
    """
    Content Metadata
    """
    id: int
    type: ContentType


class PlaylistMeta(BaseModel):
    """
    Playlist Metadata
    """
    id: int
    instanceId: int


class PlayMeta(BaseModel):
    """
    Content Play Info
    """
    startTime: datetime
    duration: float


class ErrorMeta(BaseModel):
    """
    Error Info
    """
    code: str
    message: str | None = None


class BaseEvent(BaseModel):
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

    def model_dump(
        self,
        *args,
        mode: Literal['json', 'python'] | str = 'python',
        **kwargs
    ) -> dict[str, Any]:
        kwargs['mode'] = mode
        model_dict = super().model_dump(*args, **kwargs)

        if mode == 'json':
            model_dict["sent_timestamp"] = self._sent_timestamp.isoformat()
        else:
            model_dict["sent_timestamp"] = self._sent_timestamp

        return model_dict


# final
class PingEvent(BaseEvent):
    """
    Ping Request
    contains only device metadata
    """
    type: Literal['ping']


# final
class PlayEvent(BaseEvent):
    """
    Play Event
    Contains device, content metadata and play metadata
    """
    type: Literal['play']
    content: ContentMeta
    play: PlayMeta


# final
class ErrorEvent(BaseEvent):
    """
    Error Event
    Contains device, content metadata and error
    """
    type: Literal['error']
    content: ContentMeta
    error: ErrorMeta
