from sqlalchemy.orm import Session

# infra - aux
from app.shared.infra.persistence.postgres_sql.utils.connection import connection_engine
from app.shared.infra.persistence.postgres_sql.utils.patient_register_model import PatientRegisterModel


class CreatePatientRegisterPostgress:
    def __init__(self):
        pass

    def create(self,  patient_register) -> bool:

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
