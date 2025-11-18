from sqlalchemy.orm import Session

# infra
from app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo
# infra - aux
from app.shared.infra.persistence.postgres_sql.utils.connection import connection_engine
from app.shared.infra.persistence.postgres_sql.utils.patient_register_model import PatientRegisterModel


class CreatePatientRegisterPostgress(CreatePatientRepo):
    def __init__(self):
        super().__init__()

    def create(self, patient_register) -> bool:
        try:
            db: Session = Session(connection_engine)
            patient_register_model = PatientRegisterModel(**patient_register)
            print(f"patientRegisterModel {patient_register_model}")

            db.add(patient_register_model)
            db.commit()
            return True
        except Exception as e:
            print(f"Error creating patient register: {e}")
            return False
