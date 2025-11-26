"""Handler to persist patient register on DB master."""

from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo
from src.app.shared.domain.events.domain_event_handler import DomainEventHandler


class PersistOnDbMasterHandler(DomainEventHandler):
    """Handler to persist patient register on DB master."""

    def __init__(
            self,
            susbscribed_to: str,
            create_patient_repo: CreatePatientRepo
    ):
        """Initialize the persist on DB master handler with the subscribed event name."""
        super().__init__(susbscribed_to)
        self._create_patient_repo = create_patient_repo

    def handle(self, event) -> None:
        """Handle the given domain event by persisting the patient register on DB master."""
        try:
            print("\n\n--------- PersistOnDbMasterHandler - BEGIN --------- ")
            patient_data = event.data
            # self._create_patient_repo.create_patient_register(patient_data)
            self._create_patient_repo.create(patient_data)
            print("[successfully]: persisted patient register on DB master.")
        except RuntimeError as e:
            print(f"[Error]: persisting patient register on DB master: {e}")
        finally:
            print(" --------- PersistOnDbMasterHandler - END --------- \n\n")
