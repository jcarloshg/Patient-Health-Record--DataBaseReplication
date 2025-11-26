"""Domain event for patient register creation."""


import uuid
from typing import Optional

from src.app.shared.domain.events.domain_event import DomainEvent


class PatientRegisterCreatedEvent(DomainEvent):
    """Event triggered when a patient register is created."""

    @staticmethod
    def event_name() -> str:
        """Get the name of the event. -> 'PatientRegisterCreated'"""
        return "PatientRegisterCreated"

    def __init__(
        self,
        data: dict[str, any],
        aggregate_uuid: Optional[uuid.UUID] = None
    ):
        super().__init__(
            domain_name=PatientRegisterCreatedEvent.event_name(),
            data=data,
            aggregate_uuid=aggregate_uuid
        )
