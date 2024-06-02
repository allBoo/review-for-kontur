from app.data.repository.devices import DevicesHistoryRepository
from app.data.repository.events import EventsRepository


class EventsPushService:
    def __init__(
        self,
        devices_repository: DevicesHistoryRepository,
        events_repository: EventsRepository
    ):
        self.events_repository = events_repository

    def push_event(self, event: Event):
        self.events_repository.push_event(event)
