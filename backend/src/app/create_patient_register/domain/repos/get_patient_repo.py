"""Repository interface for getting patient registration data."""

from abc import ABC, abstractmethod

from src.app.shared.domain.criteria.criteria import Criteria


class GetPatientRepo(ABC):
    """Repository interface for getting patient registration data."""

    @abstractmethod
    def get(self, criteria: Criteria) -> list:
        """Get patient registration data from the data store based on criteria."""
        raise NotImplementedError()
