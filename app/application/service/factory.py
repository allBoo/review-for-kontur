from config import settings

from application.container import ApplicationContainer
from shared.infrastructure.kafka.config import Config
from events.data.source import EventsDataSource, DlqDataSource
from events.service.router import EventRouter
from events.service.saver import EventsSaver

from .events import set_sent_timestamp, PingEventsHandler, AdPlayEventsHandler, ContentPlayEventsHandler


class ServiceFactory:

    @staticmethod
    def get_events_data_source(
            kafka_group_id: str | None = None
    ) -> EventsDataSource:
        kafka_config = Config(
            settings,
            {'topic.prefix': settings.KAFKA_TOPICS_PREFIX}
        )
        if kafka_group_id:
            kafka_config.patch('group.id', kafka_group_id)
        return EventsDataSource(kafka_config, settings.KAFKA_EVENTS_TOPIC)

    @classmethod
    def get_events_saver(cls) -> EventsSaver:
        return EventsSaver(
            storages=[
                cls.get_events_data_source()
            ],
            mutators=[
                set_sent_timestamp
            ],
        )

    @classmethod
    def get_events_router(cls) -> EventRouter:
        return EventRouter(cls.get_events_data_source())

    @staticmethod
    def get_dlq_writer() -> DlqDataSource:
        kafka_config = Config(
            settings,
            {'topic.prefix': settings.KAFKA_TOPICS_PREFIX}
        )

        return DlqDataSource(kafka_config, settings.KAFKA_DLQ_TOPIC)

    @staticmethod
    def get_ping_event_handler() -> PingEventsHandler:
        container = ApplicationContainer(settings)
        return PingEventsHandler(container)

    @staticmethod
    def get_ad_event_handler() -> AdPlayEventsHandler:
        container = ApplicationContainer(settings)
        return AdPlayEventsHandler(container)

    @staticmethod
    def get_content_event_handler() -> ContentPlayEventsHandler:
        container = ApplicationContainer(settings)
        return ContentPlayEventsHandler(container)
