"""Domain event base class."""

import uuid
from datetime import datetime, timezone
from typing import Optional


class DomainEvent:
    """Base class for domain events."""

    def __init__(
        self,
        domain_name: str,
        data: dict[str, any],
        aggregate_uuid: Optional[uuid.UUID] = None
    ):
        self._uuid: str = str(uuid.uuid4())
        self._occurred_on: datetime = datetime.now(timezone.utc)
        self.domain_name = domain_name
        self.data: dict[str, any] = data
        self.aggregate_id = aggregate_uuid

    def to_primitives(self) -> dict[str, any]:
        """Convert the event to a primitive dictionary format."""
        return {
            "uuid": self._uuid,
            "occurred_on": self._occurred_on.isoformat(),
            "domain_name": self.domain_name,
            "aggregate_id": str(self.aggregate_id) if self.aggregate_id else None,
            "data": self.data
        }
