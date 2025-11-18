
"""
Unit tests for CreatePatientRegisterUseCase
"""
from app.create_patient_register.application.create_patient_register import (
    CreatePatientRegisterUseCase,
    CreatePatientRegisterProps
)


def test_create_patient_register_invalid_data():
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
    use_case = CreatePatientRegisterUseCase()
    response = use_case.execute(props)

    # Assert
    assert response.code == 400
    assert response.is_success is False


def test_create_patient_register_out_of_range():
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
    use_case = CreatePatientRegisterUseCase()
    response = use_case.execute(props)

    # Assert
    assert response.code == 400
    assert response.is_success is False
    assert response.message == "Data validation error"
    assert response.data['user_message'] == "Invalid data"
    assert response.data['property'] == "date_of_birth"


def test_create_patient_register_valid_data():
    """Test valid patient register data."""

    # Arrange
    props = CreatePatientRegisterProps()
    props['body'] = {
        "uuid": "dbd13f36-c8a6-4398-8056-9560dbe0a917",
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1990-05-15",
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
    use_case = CreatePatientRegisterUseCase()
    response = use_case.execute(props)

    # Assert
    assert response.code == 200
    assert response.is_success is True
    assert response.message == "Patient registed successfully"
    assert response.data is not None
