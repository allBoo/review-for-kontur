from app.data.source.kafka.raw_events_kafka_data_source import RawEventsKafkaDataSource
from app.data.service.raw_events import RawEventsSaver, RawEventsReader
from app.infrastructure.kafka.config import Config
from app.config import KafkaConfig


class ServiceFactory:

    @staticmethod
    def get_raw_events_saver() -> RawEventsSaver:
        return RawEventsSaver(storages=[
            RawEventsKafkaDataSource(Config(KafkaConfig()))
        ])

    @staticmethod
    def get_raw_events_primary_reader() -> RawEventsReader:
        return RawEventsReader(storage=RawEventsKafkaDataSource(Config(KafkaConfig())))
