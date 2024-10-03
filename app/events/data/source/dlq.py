from shared.data.source import DataSource
from shared.data.source.impl.kafka import KafkaWriter, KafkaReader
from shared.infrastructure.kafka.config import Config as KafkaConfig
from shared.infrastructure.kafka.consumer import KafkaConsumer
from shared.infrastructure.kafka.producer import KafkaProducer
from events.data.models.dlq import DlqEvent


class DlqDataSource(DataSource[DlqEvent]):
    __topic = 'dlq'

    def __init__(self, config: KafkaConfig, topic: str = __topic) -> None:
        self._config: KafkaConfig = config
        self._topic = topic

    def get_writer(self) -> KafkaWriter[DlqEvent]:
        return KafkaWriter[DlqEvent](DlqEvent, KafkaProducer(
            self._config.producer_config(),
            self._config.topics(self._topic)
        ), '')

    def get_reader(self) -> KafkaReader[DlqEvent]:
        return KafkaReader[DlqEvent](DlqEvent, KafkaConsumer(
            self._config.consumer_config(),
            self._config.topics(self._topic)
        ))
