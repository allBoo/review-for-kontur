from app.data.models.models import Event


class EventsRepository:
    def push_event(self, event: Event) -> None:
        raise NotImplementedError

