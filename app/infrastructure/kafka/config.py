from typing import Callable

from app.config import KafkaConfig
import socket


class Config:

    def __init__(self, system_config: KafkaConfig) -> None:
        self.system_config = system_config

    def producer_config(self) -> dict[str, str]:
        return {
            'bootstrap.servers': self.system_config.KAFKA_SERVERS,
            'client.id': socket.gethostname()
        }

    def consumer_config(self, group_id: str) -> dict[str, str]:
        return {
            'bootstrap.servers': self.system_config.KAFKA_SERVERS,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }

    def producer_flush_interval(self) -> int:
        return self.system_config.KAFKA_PRODUCER_FLUSH_INTERVAL

    def _topic_prefix(self, prefix) -> Callable[[str], str]:
        def formatter(topic: str) -> str:
            return f'{prefix}-{topic}'
        return formatter

    def raw_topics(self) -> Callable[[str], str]:
        return self._topic_prefix(self.system_config.KAFKA_RAW_EVENTS_TOPIC)

    def raw_consumer_group(self) -> str:
        return (f'{self.system_config.KAFKA_RAW_EVENTS_CONSUMER_GROUP}-'
                f'{self.system_config.KAFKA_RAW_EVENTS_CONSUMER_GROUP_VERSION}')
