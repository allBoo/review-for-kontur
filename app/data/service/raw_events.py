import asyncio
import logging
from typing import Annotated

from annotated_types import MinLen

from app.data.models import RawBaseEvent
from app.data.source.raw_events import RawEventsDataSource

logger = logging.getLogger(__name__)


class RawEventsSaver:
    """
    Implements the business logic for saving raw events in a fail-safe way.
    """
    def __init__(self, storages: Annotated[list[RawEventsDataSource], MinLen(min_length=1)]) -> None:
        self.storages = storages

    async def save(self, raw_event: RawBaseEvent) -> None:
        storage, fallback_storages = self.storages[0], self.storages[1:]

        await storage.store_event(raw_event, on_failure=lambda event: self._save_fallback(event, fallback_storages))

    def _save_fallback(self, raw_event: RawBaseEvent, storages: list[RawEventsDataSource]) -> None:
        if not storages:
            logger.error(f"Failed to save event {raw_event}")
            return

        logger.warning(f"Failed to save event {raw_event}. Trying to save to fallback storage")

        storage, fallback_storages = storages[0], storages[1:]
        c = storage.store_event(raw_event, on_failure=lambda event: self._save_fallback(event, fallback_storages))
        asyncio.ensure_future(c)

