"""Module for create patient register route."""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.app.create_patient_register.infra.persistence.db.create_patient_register_postgress import CreatePatientRegisterPostgress
from src.app.create_patient_register.application.create_patient_register import CreatePatientRegisterProps, CreatePatientRegisterUseCase


create_patient_register_route = APIRouter()


@create_patient_register_route.post("/patient-register")
async def create_patient_register(request: Request):
    """Route to create a patient register."""

   # init use case
    create_patient_repo = CreatePatientRegisterPostgress()
    use_case = CreatePatientRegisterUseCase(create_patient_repo)
    props = CreatePatientRegisterProps()
    props['body'] = await request.json()

    # execute use case
    response = use_case.execute(props)
    response_json = response.to_JSON_response()

    # return response
    return JSONResponse(
        status_code=response_json["status_code"],
        content=response_json["content"],
    )
