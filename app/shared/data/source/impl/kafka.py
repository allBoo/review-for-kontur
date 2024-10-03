from __future__ import annotations

import asyncio
import logging
from typing import Any, Generic, TypeVar, Type, Self, Callable, AsyncGenerator

from pydantic import BaseModel, TypeAdapter, ValidationError

from shared.data.source.exceptions import InvalidData, DataSourceError
from shared.data.source.interfaces import Reader, Writer
from shared.infrastructure.kafka.consumer import KafkaConsumer
from shared.infrastructure.kafka.producer import KafkaProducer
from shared.infrastructure.kafka.serializer import KafkaDataSerializer as Serializer

TR = TypeVar('TR', bound=BaseModel, covariant=True)
TW = TypeVar('TW', bound=BaseModel)

logger = logging.getLogger(__name__)


class KafkaReader(Reader[TR]):

    def __init__(self, typ: TypeAdapter[TR], consumer: KafkaConsumer) -> None:
        self.typ = typ
        self.consumer = consumer

    def filter(self, topics: list[str] | None) -> Self:
        self.consumer.subscribe(topics if topics else [''])
        return self

    async def read_one(self) -> TR | None:
        message = self.consumer.poll()

        if message is None:
            return None

        self.consumer.commit(message)

        try:
            model = self.typ.validate_json(message)
        except ValidationError:
            raise InvalidData(message)

        return model

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[TR, None]:
        while True:
            await asyncio.sleep(0)
            message = self.consumer.poll()
            if message is None:
                continue

            decoded = self.consumer.decode(message)

            try:
                model = self.typ.validate_json(decoded)
            except ValidationError as e:
                if fail_on_error:
                    raise InvalidData(decoded)
                if not silent:
                    logger.info(f"Failed to read: {e}")
                continue

            if not model:
                continue

            yield model

            self.consumer.commit(message)

    async def close(self) -> None:
        self.consumer.close()


class KafkaWriter(Writer[TW]):

    def __init__(self, typ: Type[TW], producer: KafkaProducer, topic: str) -> None:
        self.typ = typ
        self.producer = producer
        self.topic = topic

    async def write(self, data: TW, on_failure: Callable[[TW], None] | None = None) -> TW:
        self.producer.produce(self.topic, Serializer.serialize(data), lambda t, m: on_failure(data) if on_failure else None)
        return data

    async def write_to(self, topic: str, data: TW, on_failure: Callable[[TW], None] | None = None) -> TW:
        self.producer.produce(topic, Serializer.serialize(data), lambda t, m: on_failure(data) if on_failure else None)
        return data

    async def close(self) -> None:
        self.producer.close()
