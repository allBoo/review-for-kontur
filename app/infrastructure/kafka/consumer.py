import logging
from typing import Callable, Annotated
from annotated_types import MinLen

from confluent_kafka import Consumer  # type: ignore

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, config: dict[str, str], topics_formatter: Callable[[str], str] | None = None) -> None:
        self.consumer = Consumer(config)
        self.topics_formatter = topics_formatter

    def __del__(self) -> None:
        self.consumer.unsubscribe()
        self.consumer.unassign()

    def subscribe(self, topics: Annotated[list[str], MinLen(min_length=1)]) -> None:
        self.consumer.subscribe([self.topics_formatter(t) for t in topics] if self.topics_formatter else topics)

    def poll(self, timeout: float = 1.0) -> str | None:
        message = self.consumer.poll(timeout)

        if message is None:
            return None
        if message.error():
            logger.error(f'Kafka consume error occurred: {message.error()}')
            return None

        return message.value().decode('utf-8')

    def consume(self, callback: Callable[[str], None]) -> None:
        while True:
            message = self.poll(1.0)
            if message is None:
                continue

            callback(message)
