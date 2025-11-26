"""
Docstring for app.create_patient_register.domain.repos.create_patient_repo
"""

from abc import ABC, abstractmethod


class CreatePatientRepo(ABC):
    """Repository interface for creating patient registers."""

    @abstractmethod
    def create(self, patient_register) -> bool:
        """Create a new patient register in the data store."""
        raise NotImplementedError()
