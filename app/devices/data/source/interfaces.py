from typing import Protocol, Any, TypeVar, Self, Callable

TR = TypeVar('TR', covariant=True)
TW = TypeVar('TW')


class Reader(Protocol[TR]):

    def filter(self, criteria: Any) -> Self:
        ...

    async def read_one(self) -> TR | None:
        ...


class Writer(Protocol[TW]):

    async def write(self, data: TW, on_failure: Callable[[TW], None] | None = None) -> TW:
        ...
