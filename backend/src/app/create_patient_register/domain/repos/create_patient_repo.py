from abc import ABC, abstractmethod


class CreatePatientRepo(ABC):
    @abstractmethod
    def create(self, patient_register) -> bool:
        pass
