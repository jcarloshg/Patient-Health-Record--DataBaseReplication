"""Use case for creating a patient register."""

import uuid
from typing import TypedDict, Any

# domain
from src.app.create_patient_register.domain.events.patient_register_created_event import PatientRegisterCreatedEvent
from src.app.create_patient_register.domain.models.patient_register import PatientRegister
# domain shared
from src.app.shared.domain.models.model_error_exeption import ModelErrorException
from src.app.shared.domain.models.custom_response import CustomResponse
# infra
from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo


class CreatePatientRegisterProps(TypedDict):
    """TypedDict for patient register creation properties."""
    body: dict[str, Any]


class CreatePatientRegisterUseCase:

    """Use case for creating a patient register."""

    def __init__(self, create_patient_repo: CreatePatientRepo):
        self._create_patient_repo = create_patient_repo

    def execute(self, props: CreatePatientRegisterProps) -> CustomResponse:
        """Execute the use case to create a patient register."""
        try:

            # 1. User enters patient demographic information (name, date of birth (DOB), identification number, contact details)
            # 2. User enters initial medical information (allergies, medical history, current medications)
            # 3. System validates the input data
            body = props['body']
            patient_register_data = PatientRegister(body)
            patient_register_primitives = patient_register_data.to_primitives()

            # 4. System creates the record in the primary database
            create_resp = self._create_patient_repo.create(
                patient_register_primitives)
            if not create_resp:
                return CustomResponse.error(msg="Something went wrong creating patient register")

            # 5. System replicates the record to master-slave replicas for high availability
            # 6. System asynchronously replicates to DR replica in geographically separated region
            # 6.1 create necessary data
            aggregate_uuid: uuid.UUID = uuid.uuid4()
            # 6.2 create domain event
            patient_register_created_event = PatientRegisterCreatedEvent(
                data=patient_register_primitives,
                aggregate_uuid=aggregate_uuid
            )

            # 7. System confirms successful creation and returns patient ID
            return CustomResponse.success(
                msg="Patient register created successfully",
                data=patient_register_primitives
            )

        except ModelErrorException as e:
            primitives = e.primitives()
            return CustomResponse.error(msg="Data validation error", data=primitives)
        except Exception as e:
            """Handle unexpected errors."""
            return CustomResponse.error(msg="Internal server error", data={})
