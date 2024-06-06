from abc import ABC, abstractmethod
from typing import Callable

from .interfaces import Reader
from ..models import RawBaseEvent


class RawEventsDataSource(ABC):

    @abstractmethod
    async def store_event(self, event: RawBaseEvent, on_failure: Callable[[RawBaseEvent], None] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_reader(self) -> Reader[RawBaseEvent]:
        raise NotImplementedError
