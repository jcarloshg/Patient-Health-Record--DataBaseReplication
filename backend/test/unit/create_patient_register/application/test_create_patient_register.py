from app.create_patient_register.application.create_patient_register import CreatePatientRegisterProps, CreatePatientRegisterUseCase

# invalid data -> date_of_birth wrong format


def test():
    # arrage
    props = CreatePatientRegisterProps()
    props['body'] = {
        "uuid": "dbd13f36-c8a6-4398-8056-9560dbe0a917",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1980-01-1998",
    }

    # act
    use_case = CreatePatientRegisterUseCase()
    respo = use_case.execute(props)

    # assert
    assert respo.code == 400
    assert respo.is_success == False
    assert respo.message == "Data validation error"
    assert respo.data['user_message'] == "Invalid data"
    assert respo.data['property'] == "date_of_birth"
