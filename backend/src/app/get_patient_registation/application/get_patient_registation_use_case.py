""""""

from typing import TypedDict
from src.app.shared.domain.criteria.criteria import Criteria
from src.app.shared.domain.models.custom_response import CustomResponse


class GetPatientRegistationProps(TypedDict):
    """TypedDict for getting patient registration properties."""
    criteria: Criteria


class GetPatientRegistationUseCase:
    """Use case for getting patient registration."""

    def execute(self, props: GetPatientRegistationProps) -> CustomResponse:
        """Use case for getting patient registration."""
        try:
            return CustomResponse.success(
                msg="Get patient registration use case executed successfully",
                data={
                    # "props": props,
                    "patient_registrations": []
                }
            )
        except RuntimeError:
            return CustomResponse.error(msg="An error occurred while executing the use case")
