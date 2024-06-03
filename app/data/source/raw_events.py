from abc import ABC, abstractmethod
from typing import Callable

from ..models import RawBaseEvent


class RawEventsDataSource(ABC):

    @abstractmethod
    async def store_event(self, event: RawBaseEvent, on_failure: Callable[[RawBaseEvent], None] | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_next_event(self) -> RawBaseEvent | None:
        raise NotImplementedError
