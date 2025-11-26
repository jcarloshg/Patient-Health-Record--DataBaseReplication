""""Logging handler for domain events in patient register creation."""

from src.app.shared.domain.events.domain_event_handler import DomainEventHandler


class LogginHandler(DomainEventHandler):
    """Handler for logging domain events."""

    def __init__(self, susbscribed_to: str):
        """Initialize the logging handler with the subscribed event name."""
        super().__init__(susbscribed_to)

    def handle(self, event) -> None:
        """Handle the given domain event by logging its details."""
        print("\n\n--------- LogginHandler - BEGIN --------- ")
        print(
            f"Logging Event - Name: {event.domain_name}, Aggregate UUID: {event.aggregate_id if hasattr(event, 'aggregate_id') else 'N/A'}")
        print(" --------- LogginHandler - END --------- \n\n")
