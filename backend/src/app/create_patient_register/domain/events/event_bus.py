"""Event bus implementation for domain events."""


# from src.app.shared.domain.events.domain_event_handler import DomainEventHandler
# from src.app.shared.domain.events.domain_event import DomainEvent

from src.app.shared.domain.events.domain_event_handler import DomainEventHandler
from src.app.shared.domain.events.domain_event import DomainEvent


class EventBus:
    """A simple event bus to handle domain events."""

    def __init__(self):
        self._subscribers: dict[str, list] = {}

    def subscribe(self, handler: DomainEventHandler):
        """Subscribe a handler to an event."""
        event_name: str = handler.susbscribed_to
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, domain_event: DomainEvent):
        """Publish an event to all subscribed handlers."""
        event_name = domain_event.domain_name
        if event_name in self._subscribers:
            for event_handler in self._subscribers[event_name]:
                event_handler.handle(domain_event)
