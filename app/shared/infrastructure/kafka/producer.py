from __future__ import annotations

import logging
from typing import Callable

from confluent_kafka import Producer, Message, KafkaError


logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(
            self,
            producer_config: dict[str, str],
            topics_formatter: Callable[[str], str] | None = None,
            flush_interval: int = 100
    ) -> None:
        self.producer = Producer(producer_config)
        self.topics_formatter = topics_formatter

        self._flush_interval = flush_interval
        self._cntr = 0

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self.producer.poll(0)
        self.producer.flush()

    def produce(self, topic: str, message: str, on_fail: Callable[[str, str], None]) -> bool:
        result = False
        topic_name = self.topics_formatter(topic) if self.topics_formatter else topic
        try:
            try:
                self._produce(topic_name, message, on_fail)
                result = True
            except BufferError:
                logger.warning('Producer queue is full, waiting for messages to be delivered')
                self.producer.poll(0)
                self._produce(topic_name, message, on_fail)
                result = True
        except Exception as e:
            logger.error(f'Failed to produce message to topic {topic_name}: {e}')
            on_fail(topic_name, message)

        self._cntr += 1
        if self._cntr % self._flush_interval == 0:
            self.producer.poll(0)
            self.producer.flush()

        return result

    def _produce(self, topic: str, message: str, on_fail: Callable[[str, str], None]) -> None:
        self.producer.produce(topic, message, on_delivery=lambda err, msg: self._delivery_report(err, msg, on_fail))

    def _delivery_report(self, err: KafkaError | None, msg: Message, on_fail: Callable[[str, str], None]) -> None:
        if err is not None:
            logger.error(f'Message delivery to Kafka failed: {err}')
            # Retry on fail
            on_fail(msg.topic(), msg.value().decode('utf-8'))
        else:
            # logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
            pass
