from __future__ import annotations

from typing import Callable

from pydantic import KafkaDsn

from config import Config as AppConfig
import socket


class Config:

    def __init__(self, app_config: AppConfig, custom_config: dict[str, str] | None = None) -> None:
        self.app_config: AppConfig = app_config
        self.config: dict[str, str] = custom_config.copy() if custom_config else {}

    def patch(self, key: str, value: str):
        self.config[key] = value

    def producer_config(self) -> dict[str, str]:
        return {
            'bootstrap.servers': self.config.get('bootstrap.servers',
                                                 self.__kafka_host(self.app_config.KAFKA_DSN)),
            'client.id': self.config.get('client.id', socket.gethostname()),
            **self._sasl_config(),
        }

    def consumer_config(self) -> dict[str, str]:
        return {
            'bootstrap.servers': self.config.get('bootstrap.servers',
                                                 self.__kafka_host(self.app_config.KAFKA_DSN)),
            'group.id': self.config.get('group.id', self.app_config.KAFKA_CONSUMER_GROUP),
            'auto.offset.reset': self.config.get('auto.offset.reset', 'earliest'),
            'enable.auto.commit': self.config.get('enable.auto.commit', '0'),
            **self._sasl_config(),
        }

    def _sasl_config(self) -> dict[str, str]:
        if self.app_config.KAFKA_USE_SSL:
            return {
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'SCRAM-SHA-512',
                'sasl.username': self.__kafka_username(self.app_config.KAFKA_DSN),
                'sasl.password': self.__kafka_password(self.app_config.KAFKA_DSN),
                'ssl.ca.location': self.app_config.CA_LOCATION,
            }
        return {}

    def producer_flush_interval(self) -> int:
        return self.app_config.KAFKA_PRODUCER_FLUSH_INTERVAL

    def _suffixed_topic(self, topic: str) -> Callable[[str], str]:
        def formatter(suffix: str) -> str:
            return f'{topic}.{suffix}' if suffix else topic
        return formatter

    def topics(self, topic_base_name: str) -> Callable[[str], str]:
        prefix = self.config.get('topic.prefix', self.app_config.KAFKA_TOPICS_PREFIX)
        return self._suffixed_topic(f'{prefix}.{topic_base_name}')

    def topic(self, topic_base_name: str) -> str:
        return self.topics(topic_base_name)('')

    def __kafka_host(self, dsn: KafkaDsn) -> str:
        return f'{dsn.host}:{dsn.port}'

    def __kafka_username(self, dsn: KafkaDsn) -> str:
        return dsn.username or ''

    def __kafka_password(self, dsn: KafkaDsn) -> str:
        return dsn.password or ''
