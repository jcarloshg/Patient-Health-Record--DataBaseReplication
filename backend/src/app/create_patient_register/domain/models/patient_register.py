from typing import Any
from pydantic import BaseModel, UUID4, Field, ValidationError, field_validator
from datetime import date

# domain
from src.app.shared.domain.models.model_error_exeption import ModelErrorException


class PatientInformationData(BaseModel):

    uuid: UUID4 = Field(..., description="Unique identifier for the patient")

    # personal data
    first_name: str = Field(...,
                            min_length=1,
                            max_length=50,
                            description="Patient's first name"
                            )
    last_name: str = Field(...,
                           min_length=1,
                           max_length=50,
                           description="Patient's last name"
                           )

    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        """Validate that date_of_birth is a valid past date."""
        min_date = date(1900, 1, 1)
        max_date = date.today()
        if not (min_date <= value <= max_date):
            raise ValueError(
                f"date_of_birth must be between {min_date} and {max_date}")
        return value
    date_of_birth: date = Field(...,
                                description="Date of birth in YYYY-MM-DD format"
                                )

    # # contact details
    email: str = Field(...,
                       pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$",
                       description="Patient's email address")
    phone_number: str = Field(...,
                              min_length=10,
                              max_length=15,
                              description="Patient's phone number")
    address: str = Field(...,
                         min_length=1,
                         max_length=100,
                         description="Patient's address")
    emergency_contact: str = Field(...,
                                   min_length=1,
                                   max_length=50,
                                   description="Emergency contact details")
    # # medical information
    allergies: list[str] = Field(
        default_factory=list,
        description="List of patient allergies")
    medical_history: list[str] = Field(
        default_factory=list,
        description="Patient's medical history")
    current_medications: list[str] = Field(
        default_factory=list,
        description="Current medications patient is taking")


class PatientRegister:
    """Patient Register Domain Model"""

    def __init__(self, data: dict[str, Any]):
        try:
            self._data: PatientInformationData = PatientInformationData(**data)
        except ValidationError as e:
            property_name = e.errors()[0]['loc'][0]
            developer_message = e.errors()[0]['msg']
            raise ModelErrorException(
                developer_message=developer_message,
                property_name=property_name
            ) from e

    def to_primitives(self) -> dict[str, Any]:
        """Convert the model to primitive dictionary format."""
        model_dump = self._data.model_dump(mode="json")
        return model_dump
