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

    def producer_flush_interval(self) -> int:
        return self.system_config.KAFKA_PRODUCER_FLUSH_INTERVAL

    def raw_topic(self, suffix: str) -> str:
        return f'{self.system_config.KAFKA_RAW_EVENTS_TOPIC}-{suffix}'

