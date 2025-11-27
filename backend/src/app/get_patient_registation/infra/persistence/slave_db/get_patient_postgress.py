""""PostgreSQL implementation of GetPatientRepo."""

from sqlalchemy.orm import Session
from sqlalchemy import text

# domain - repos
from src.app.create_patient_register.domain.models.patient_register import PatientInformationData
from src.app.create_patient_register.domain.repos.get_patient_repo import GetPatientRepo
from src.app.shared.domain.criteria.criteria_to_sql import CriteriaToSQL

# infra - aux
from src.app.shared.infra.persistence.slave_postgres_sql.utils.slave_connection import slave_connection_engine
from src.app.shared.infra.persistence.main_postgres_sql.utils.patient_register_model import PatientRegisterModel


class GetPatientPostgress(GetPatientRepo):
    """PostgreSQL implementation of GetPatientRepo."""

    def __init__(self):
        """Initialize GetPatientPostgress repository."""
        super().__init__()

    def get(self, criteria) -> list:

        try:
            db: Session = Session(slave_connection_engine)

            criteria_to_sql = CriteriaToSQL()
            # query_str, params = criteria_to_sql.criteria_to_sql_parametrized(
            #     criteria
            # )

            sql_query = "SELECT * FROM patientregister LIMIT 100"

            result = db.execute(text(sql_query))
            # Convert result to list of dictionaries
            rows = result.fetchall()
            columns = result.keys()
            result_dicts = [dict(zip(columns, row, strict=True))
                            for row in rows]

            patient_register: list[dict] = []
            for row in result_dicts:
                uuid_value = row.get('uuid')
                if uuid_value is not None:
                    uuid_value = str(uuid_value)
                patient_data = PatientInformationData(
                    uuid=uuid_value,
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                    date_of_birth=row.get('date_of_birth'),
                    email=row.get('email'),
                    phone_number=row.get('phone_number'),
                    address=row.get('address'),
                    emergency_contact=row.get('emergency_contact'),
                    allergies=row.get('allergies'),
                    medical_history=row.get('medical_history'),
                    current_medications=row.get('current_medications')
                )

                # Convert to dict for JSON serialization
                patient_register.append(patient_data.__dict__)

            # print(f"sql_query {sql_query}")
            # result = db.execute(text(sql_query), params)

            # print(result)
            # print(f"result {result.keys()}")

            # patient_rows = result.fetchall()

            # Use result.mappings() to get dict-like access to columns
            # for row in result.mappings():
            #     print(f"row {row}")
            #     patient_data = PatientInformationData(
            #         uuid=row['uuid'],
            #         first_name=row['first_name'],
            #         last_name=row['last_name'],
            #         date_of_birth=row['date_of_birth'],
            #         email=row['email'],
            #         phone_number=row['phone_number'],
            #         address=row['address'],
            #         emergency_contact=row['emergency_contact'],
            #         allergies=row['allergies'],
            #         medical_history=row['medical_history'],
            #         current_medications=row['current_medications']
            #     )
            #     patient_register.append(patient_data)

            return patient_register

        except Exception as e:
            print(f"Error getting patient registration data: {e}")
            return []
