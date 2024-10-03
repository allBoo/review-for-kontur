import logging
from typing import Callable

from events.data.models.events import BaseEvent, PingEvent, PlayEvent, ErrorEvent, ContentType
from events.data.source.events import EventsDataSource

logger = logging.getLogger(__name__)

PingRoute: str = 'ping'
ErrorRoute: str = 'error'
AdPlaysRoute: str = 'ad-play'
ContentPlaysRoute: str = 'content-play'

RouteMap: dict[type[BaseEvent], Callable[[BaseEvent], str]] = {
    PingEvent: lambda event: PingRoute,
    ErrorEvent: lambda event: ErrorRoute,
    PlayEvent: lambda event: ContentPlaysRoute if event.content.type == ContentType.CONTENT else AdPlaysRoute
}


class EventRouter:

    def __init__(self, writer: EventsDataSource) -> None:
        self._writer = writer.get_writer()

    async def handle(self, event: BaseEvent) -> bool:
        router = RouteMap.get(type(event))
        if not router:
            logger.warning(f'No route found for event {event.type}')
            return False

        route_name = router(event)
        if not route_name:
            logger.warning(f'No route found for event {event.type}')
            return False

        logger.debug(f'Route event {event.type} to {route_name}')
        await self._writer.write_to(route_name, event)

        return True

    async def close(self):
        await self._writer.close()

