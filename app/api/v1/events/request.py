from app.data.models import RawPingEvent, RawPlayEvent, RawErrorEvent


# final
class PingRequest(RawPingEvent):
    """
    Ping Request
    contains only device metadata
    """
    ...


# final
class PlayEventRequest(RawPlayEvent):
    """
    Play Event
    Contains device, content metadata and play metadata
    """
    ...


# final
class ErrorEventRequest(RawErrorEvent):
    """
    Error Event
    Contains device, content metadata and error
    """
    ...
