import logging
from datetime import datetime, timezone

from events.data.models import Event
from shared.container import Container

logger = logging.getLogger(__name__)


def set_sent_timestamp(event: Event) -> Event:
    """
    Set sent_timestamp to current datetime in UTC timezone
    :param event: BaseEvent
    :return: RawBaseEvent
    """
    event.sent_timestamp = datetime.now(timezone.utc)
    return event


class PingEventsHandler:

    def __init__(self, container: Container):
        self.container = container

    async def handle(self, event: Event) -> bool:
        logger.info(f'Handle PING event {event}')
        return False


class AdPlayEventsHandler:

    def __init__(self, container: Container):
        self.container = container

    async def handle(self, event: Event) -> bool:
        logger.info(f'Handle AdPlay event {event}')
        return False


class ContentPlayEventsHandler:

    def __init__(self, container: Container):
        self.container = container

    async def handle(self, event: Event) -> bool:
        logger.info(f'Handle ContentPlay event {event}')
        return False
