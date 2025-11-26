"""
    Replicate Patient Register Postgress Repo Implementation
"""

from sqlalchemy.orm import Session

from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo
from src.app.shared.infra.persistence.slave_postgres_sql.utils.slave_connection import slave_connection_engine
from src.app.shared.infra.persistence.slave_postgres_sql.utils.patient_register_model import PatientRegisterModel


class ReplicatePatientRegisterPostgress(CreatePatientRepo):
    """Class to replicate patient register in Postgres database."""

    def __init__(self):
        """Initialize ReplicatePatientRegisterPostgress repository."""
        super().__init__()

    def create(self, patient_register: dict[str, any]) -> bool:
        """Replicate a patient register in the Postgres database."""
        try:
            db: Session = Session(slave_connection_engine)
            patient_register_model = PatientRegisterModel(**patient_register)
            print(f"patientRegisterModel {patient_register_model}")

            db.add(patient_register_model)
            db.commit()
            return True
        except Exception as e:
            """hola"""
            print(f"Error replicating patient register: {e}")
            return False
