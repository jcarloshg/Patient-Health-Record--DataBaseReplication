
"""
Unit tests for CreatePatientRegisterUseCase
"""

import uuid
import pytest

from src.app.create_patient_register.domain.repos.create_patient_repo import CreatePatientRepo
from src.app.create_patient_register.infra.persistence.main_db.create_patient_register_postgress import CreatePatientRegisterPostgress
from src.app.create_patient_register.application.create_patient_register import (
    CreatePatientRegisterUseCase,
    CreatePatientRegisterProps
)


class TestCreatePatientRegister:
    """Instance variables will be initialized in setup_method"""

    def setup_method(self, method):
        """Setup code before each test."""
        createPatientRegisterPostgress = CreatePatientRegisterPostgress()
        self.create_patient_repo = createPatientRegisterPostgress
        self.use_case = CreatePatientRegisterUseCase(self.create_patient_repo)

    def teardown_method(self, method):
        """Teardown code after each test."""
        pass

    def test_create_patient_register_invalid_data(self):
        """Test invalid patient register data (wrong date_of_birth format)."""

        # Arrange
        props = CreatePatientRegisterProps()
        props['body'] = {
            "uuid": "dbd13f36-c8a6-4398-8056-9560dbe0a917",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-1998",
            # contact data
            "email": "jane.smith@example.com",
            "phone_number": "1234567890",
            "address": "123 Main St, Springfield",
            "emergency_contact": "John Smith",
            # medical data
            "allergies": ["penicillin"],
            "medical_history": ["hypertension"],
            "current_medications": ["lisinopril"]
        }

        # Act
        response = self.use_case.execute(props)

        # Assert
        assert response.code == 400
        assert response.is_success is False

    def test_create_patient_register_out_of_range(self):
        """Test patient register data with out-of-range date_of_birth."""

        # Arrange
        props = CreatePatientRegisterProps()
        props['body'] = {
            "uuid": "dbd13f36-c8a6-4398-8056-9560dbe0a917",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1880-01-01",
            # contact data
            "email": "jane.smith@example.com",
            "phone_number": "1234567890",
            "address": "123 Main St, Springfield",
            "emergency_contact": "John Smith",
            # medical data
            "allergies": ["penicillin"],
            "medical_history": ["hypertension"],
            "current_medications": ["lisinopril"]
        }

        # Act
        response = self.use_case.execute(props)

        # Assert
        assert response.code == 400
        assert response.is_success is False
        assert response.message == "Data validation error"
        assert response.data['user_message'] == "Invalid data"
        assert response.data['property'] == "date_of_birth"

    def test_create_patient_register_valid_data(self):
        """Test valid patient register data."""

        # Arrange
        props = CreatePatientRegisterProps()
        props['body'] = {
            "uuid": str(uuid.uuid4()),
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1990-05-15",
            # contact data
            "email": "jane.smith@example.com",
            "phone_number": "1234567890",
            "address": "123 Main St, Springfield",
            "emergency_contact": "John Smith",
            # medical data
            "allergies": ["penicillin", "latex"],
            "medical_history": ["hypertension", "asthma"],
            "current_medications": ["lisinopril", "albuterol"]
        }

        # Act
        response = self.use_case.execute(props)

        # Assert
        assert response.code == 200
        assert response.is_success is True
        assert response.message == "Patient register created successfully"
        assert response.data is not None
