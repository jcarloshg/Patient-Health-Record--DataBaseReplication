"""Domain event handler base class."""

from src.app.shared.domain.events.domain_event import DomainEvent


class DomainEventHandler:
    """Base class for domain event handlers."""

    def __init__(self, susbscribed_to: str):
        self.susbscribed_to = susbscribed_to

    def handle(self, event: DomainEvent) -> None:
        """Handle the given domain event."""
        raise NotImplementedError("Subclasses must implement this method.")
