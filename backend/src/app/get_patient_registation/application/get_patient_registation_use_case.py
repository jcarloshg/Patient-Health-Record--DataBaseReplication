"""Get Patient Registration Use Case Module."""

from typing import TypedDict
# domain
from src.app.create_patient_register.domain.repos.get_patient_repo import GetPatientRepo
# infra
from src.app.shared.domain.criteria.criteria import Criteria
from src.app.shared.domain.models.custom_response import CustomResponse


class GetPatientRegistationProps(TypedDict):
    """TypedDict for getting patient registration properties."""
    criteria: Criteria


class GetPatientRegistationUseCase:
    """Use case for getting patient registration."""

    def __init__(self, get_patient_repo: GetPatientRepo):
        """Initialize GetPatientRegistationUseCase."""
        self.get_patient_repo = get_patient_repo

    def execute(self, props: GetPatientRegistationProps) -> CustomResponse:
        """Use case for getting patient registration."""
        try:

            criteria = props["criteria"]
            patient_registrations = self.get_patient_repo.get(criteria)
            patient_registrations_primitives = [
                registration.to_primitives() for registration in patient_registrations
            ]

            return CustomResponse.success(
                msg="Get patient registration use case executed successfully",
                data={
                    "registrations": patient_registrations_primitives
                }
            )
        except RuntimeError:
            return CustomResponse.error(msg="An error occurred while executing the use case")
