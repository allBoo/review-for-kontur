from typing import Any, Generic, TypeVar, Type, Self

from pydantic import BaseModel

from app.infrastructure.kafka.consumer import KafkaConsumer

T = TypeVar('T', bound=BaseModel, covariant=True)


class KafkaReader(Generic[T]):

    def __init__(self, typ: Type[T], consumer: KafkaConsumer) -> None:
        self.typ = typ
        self.consumer = consumer

    def filter(self, topics: list[str]) -> Self:
        self.consumer.subscribe(topics)
        return self

    async def read_one(self) -> T | None:
        message = self.consumer.poll(1.0)

        if message is None:
            return None

        return self.typ.parse_raw(message)
