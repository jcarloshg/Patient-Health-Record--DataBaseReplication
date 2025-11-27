""""PostgreSQL implementation of GetPatientRepo."""

from sqlalchemy.orm import Session
from sqlalchemy import text

# domain - repos
from src.app.create_patient_register.domain.models.patient_register import PatientInformationData, PatientRegister
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

    def get(self, criteria) -> list[PatientRegister]:

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
            result_dicts = [dict(zip(columns, row)) for row in rows]

            patient_register_list: list[PatientRegister] = []

            for row in result_dicts:
                try:

                    # parse uuid to string
                    uuid_value = row.get('uuid')
                    if uuid_value is not None:
                        uuid_value = str(uuid_value)
                    row["uuid"] = uuid_value

                    # parse row into PatientRegister and convert to dict
                    patient_register_parsed = PatientRegister(row)
                    patient_register_list.append(patient_register_parsed)

                except Exception as e:
                    print(f"Error creating PatientRegister: {e}")
                    continue

            return patient_register_list

        except Exception as e:
            print(f"Error getting patient registration data: {e}")
            return []
