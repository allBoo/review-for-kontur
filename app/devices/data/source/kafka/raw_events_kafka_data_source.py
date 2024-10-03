from typing import Callable

from app.data.models import RawBaseEvent
from app.data.source.interfaces import Reader, Writer
from app.data.source.raw_events import RawEventsDataSource
from app.infrastructure.kafka.config import Config as KafkaConfig
from app.infrastructure.kafka.consumer import KafkaConsumer
from app.infrastructure.kafka.producer import KafkaProducer
from app.infrastructure.kafka.serializer import KafkaDataSerializer as Serializer

from .reader import KafkaReader


class RawEventsKafkaDataSource(RawEventsDataSource):
    def __init__(self, config: KafkaConfig) -> None:
        self._config: KafkaConfig = config
        self._producer: KafkaProducer | None = None  # lazy init

    @property
    def producer(self) -> KafkaProducer:
        if self._producer is None:
            self._producer = KafkaProducer(self._config)
        return self._producer

    async def store_event(self, event: RawBaseEvent, on_failure: Callable[[RawBaseEvent], None] | None = None) -> None:
        topic: str = self._config.raw_topics()(event.type)
        self.producer.produce(topic, Serializer.serialize(event), lambda t, m: on_failure(event) if on_failure else None)

    def get_writer(self) -> Writer[RawBaseEvent]:
        return self.producer

    def get_reader(self) -> Reader[RawBaseEvent]:
        return KafkaReader(RawBaseEvent, KafkaConsumer(
                self._config.consumer_config(self._config.raw_consumer_group()),
                self._config.raw_topics()
            ))
