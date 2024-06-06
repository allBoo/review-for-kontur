from typing import Protocol, Any, TypeVar, Self

T = TypeVar('T', covariant=True)


class Reader(Protocol[T]):

    def filter(self, criteria: Any) -> Self:
        ...

    async def read_one(self) -> T | None:
        ...
