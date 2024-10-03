import asyncio
import logging
from typing import Annotated, TypeVar, Callable

from annotated_types import MinLen

from events.data.models.events import Event
from events.data.source.events import EventsDataSource
from shared.data.interfaces import Mutator, Validator
from shared.data.source import Writer

logger = logging.getLogger(__name__)


class EventsSaver:
    """
    Implements the business logic for saving raw events in a fail-safe way to the chain of storages.
    """
    def __init__(
        self,
        storages: Annotated[list[EventsDataSource], MinLen(min_length=1)],
        validators: Annotated[list[Validator[Event]], MinLen(min_length=1)] | None = None,
        mutators: Annotated[list[Mutator[Event]], MinLen(min_length=1)] | None = None,
    ) -> None:
        self.storages = [s.get_writer() for s in storages]
        self.validators: list[Validator[Event]] = validators or []
        self.mutators: list[Mutator[Event]] = mutators or []

    async def save(self, event: Event) -> None:
        for mutator in self.mutators:
            event = mutator(event)

        for validator in self.validators:
            if not validator(event):
                raise ValueError(f"Event {event} is not valid by validator {validator}")

        storage, fallback_storages = self.storages[0], self.storages[1:]
        try:
            await storage.write(event, on_failure=lambda event: self._save_fallback(event, fallback_storages))
        except Exception as e:
            if fallback_storages:
                logger.exception(f"Error while saving event {event} to storage {storage}. Trying to save to fallback storage")
                self._save_fallback(event, fallback_storages, silent=True)
            else:
                logger.exception(f"Failed to save event {event}")

    def _save_fallback(self, event: Event, storages: list[Writer], silent: bool = False) -> None:
        if not storages:
            return

        if not silent:
            logger.warning(f"Failed to save event {event}. Trying to save to fallback storage")

        storage, fallback_storages = storages[0], storages[1:]
        try:
            c = storage.write(event, on_failure=lambda event: self._save_fallback(event, fallback_storages))
            asyncio.ensure_future(c)
        except Exception as e:
            if fallback_storages:
                logger.exception(f"Error while saving event {event} to fallback storage {storage}. Trying to save to another fallback storage")
                self._save_fallback(event, fallback_storages, silent=True)
            else:
                logger.exception(f"Failed to save event {event}")
