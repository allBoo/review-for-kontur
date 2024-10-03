from shared.data.source import DataSource
from shared.data.source.impl.kafka import KafkaWriter, KafkaReader
from shared.infrastructure.kafka.config import Config as KafkaConfig
from shared.infrastructure.kafka.consumer import KafkaConsumer
from shared.infrastructure.kafka.producer import KafkaProducer
from events.data.models.events import Event, EventAdapter


class EventsDataSource(DataSource[Event]):
    __topic = 'events'

    def __init__(self, config: KafkaConfig, topic: str = __topic) -> None:
        self._config: KafkaConfig = config
        self._topic = topic

    def get_writer(self) -> KafkaWriter[Event]:
        return KafkaWriter[Event](Event, KafkaProducer(
            self._config.producer_config(),
            self._config.topics(self._topic)
        ), '')

    def get_reader(self) -> KafkaReader[Event]:
        return KafkaReader[Event](EventAdapter, KafkaConsumer(
            self._config.consumer_config(),
            self._config.topics(self._topic)
        ))
