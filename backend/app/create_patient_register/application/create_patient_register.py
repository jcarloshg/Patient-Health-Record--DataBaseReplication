from typing import TypedDict, Any

# domain
from app.create_patient_register.domain.models.patient_register import PatientRegister
# domain shared
from app.shared.domain.models.model_error_exeption import ModelErrorException
from app.shared.domain.models.custom_response import CustomResponse
# infra
from app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo


class CreatePatientRegisterProps(TypedDict):
    body: dict[str, Any]


class CreatePatientRegisterUseCase:
    def __init__(self, create_patient_repo: CreatePatientRepo):
        self.create_patient_repo = create_patient_repo
        pass

    def execute(self, props: CreatePatientRegisterProps) -> CustomResponse:
        try:

            # 1. User enters patient demographic information (name, date of birth (DOB), identification number, contact details)
            # 2. User enters initial medical information (allergies, medical history, current medications)
            # 3. System validates the input data
            body = props['body']
            patient_register_data = PatientRegister(body)

            # 4. System creates the record in the primary database
            create_resp = self.create_patient_repo.create(
                patient_register_data.to_primitives()
            )
            if not create_resp:
                return CustomResponse.error(msg="Something went wrong creating patient register")

            return CustomResponse.success(
                msg="Patient register created successfully",
                data=patient_register_data.to_primitives()
            )
            # 5. System replicates the record to master-slave replicas for high availability
            # 6. System asynchronously replicates to DR replica in geographically separated region
            # 7. System confirms successful creation and returns patient ID

        except ModelErrorException as e:
            primitives = e.primitives()
            return CustomResponse.error(msg="Data validation error", data=primitives)
