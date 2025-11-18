from typing import TypedDict, Any

# domain
from app.create_patient_register.domain.models.patient_register import PatientRegister
# domain shared
from app.shared.domain.models.model_error_exeption import ModelErrorException
from app.shared.domain.models.custom_response import CustomResponse


class CreatePatientRegisterProps(TypedDict):
    body: dict[str, Any]


class CreatePatientRegisterUseCase:
    def __init__(self):
        pass

    def execute(self, props: CreatePatientRegisterProps) -> CustomResponse:
        try:

            # 1. User enters patient demographic information (name, date of birth (DOB), identification number, contact details)
            # 2. User enters initial medical information (allergies, medical history, current medications)
            # 3. System validates the input data
            body = props['body']
            patientRegister = PatientRegister(body)
            return CustomResponse.success(
                msg="Patient registed successfully",
                data=patientRegister
            )

            # 5. System replicates the record to master-slave replicas for high availability
            # 6. System asynchronously replicates to DR replica in geographically separated region
            # 7. System confirms successful creation and returns patient ID

        except ModelErrorException as e:
            primitives = e.primitives()
            return CustomResponse.error(msg="Data validation error", data=primitives)
