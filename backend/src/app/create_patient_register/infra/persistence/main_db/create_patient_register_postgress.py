""""Module to create patient register in Postgres database."""

from sqlalchemy.orm import Session

# # domain - repos
from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo

# # infra - aux
from src.app.shared.infra.persistence.main_postgres_sql.utils.connection import connection_engine
from src.app.shared.infra.persistence.main_postgres_sql.utils.patient_register_model import PatientRegisterModel


class CreatePatientRegisterPostgress(CreatePatientRepo):
    """Class to create patient register in Postgres database."""

    def __init__(self):
        """Initialize CreatePatientRegisterPostgress repository."""
        super().__init__()

    def create(self, patient_register: dict[str, any]) -> bool:
        """Create a patient register in the Postgres database."""
        try:
            db: Session = Session(connection_engine)
            patient_register_model = PatientRegisterModel(**patient_register)
            print(f"patientRegisterModel {patient_register_model}")

            db.add(patient_register_model)
            db.commit()
            return True
        except Exception as e:
            """hola"""
            print(f"Error creating patient register: {e}")
            return False
