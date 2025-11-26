""""Domain handler to replicate patient register on DB slave."""

from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo
from src.app.shared.domain.events.domain_event_handler import DomainEventHandler


class ReplicateRecordOnSlaveHandler(DomainEventHandler):
    """Handler to replicate patient register on DB slave."""

    def __init__(
        self,
        susbscribed_to: str,
        replicate_patient_repo: CreatePatientRepo
    ):
        """Initialize the persist on DB master handler with the subscribed event name."""
        super().__init__(susbscribed_to)
        self._replicate_patient_repo = replicate_patient_repo

    def handle(self, event) -> None:
        """Handle the given domain event by replicating the patient register on DB slave."""
        try:
            print("\n\n--------- ReplicateRecordOnSlaveHandler - BEGIN --------- ")
            registe_data = event.data
            self._replicate_patient_repo.create(registe_data)
            print("[successfully]: replicated patient register on DB slave.")
        except RuntimeError as e:
            print(f"[Error]: replicating patient register on DB slave: {e}")
        finally:
            print(" --------- ReplicateRecordOnSlaveHandler - END --------- \n\n")
