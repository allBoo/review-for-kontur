import logging
from typing import Callable

from confluent_kafka import Producer, Message, KafkaError

from .config import Config


logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.producer = Producer(config.producer_config())
        self._cntr = 0

    def __del__(self) -> None:
        self.producer.flush()

    def produce(self, topic: str, message: str, on_fail: Callable[[str, str], None]) -> None:
        try:
            try:
                self._produce(topic, message, on_fail)
            except BufferError:
                logger.warning('Producer queue is full, waiting for messages to be delivered')
                self.producer.poll(0)
                self._produce(topic, message, on_fail)
        except Exception as e:
            logger.error(f'Failed to produce message to topic {topic}: {e}')
            on_fail(topic, message)

        self._cntr += 1
        if self._cntr % self.config.producer_flush_interval() == 0:
            self.producer.poll(0)

    def _produce(self, topic: str, message: str, on_fail: Callable[[str, str], None]) -> None:
        self.producer.produce(topic, message, on_delivery=lambda err, msg: self._delivery_report(err, msg, on_fail))

    def _delivery_report(self, err: KafkaError | None, msg: Message, on_fail: Callable[[str, str], None]) -> None:
        if err is not None:
            logger.error(f'Message delivery to Kafka failed: {err}')
            # Retry on fail
            on_fail(msg.topic(), msg.value().decode('utf-8'))
        else:
            logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
