from events.data.models import PingEvent, PlayEvent, ErrorEvent


# final
class PingRequest(PingEvent):
    """
    Ping Request
    contains only device metadata
    """
    ...


# final
class PlayEventRequest(PlayEvent):
    """
    Play Event
    Contains device, content metadata and play metadata
    """
    ...


# final
class ErrorEventRequest(ErrorEvent):
    """
    Error Event
    Contains device, content metadata and error
    """
    ...
