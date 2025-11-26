"""Module for create patient register route."""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.app.create_patient_register.infra.persistence.db.create_patient_register_postgress import CreatePatientRegisterPostgress
from src.app.create_patient_register.application.create_patient_register import CreatePatientRegisterUseCase


create_patient_register_route = APIRouter()


@create_patient_register_route.post("/patient-register")
async def create_patient_register(request: Request):
    """Route to create a patient register."""

    try:
        body = await request.json()

        # init use case
        create_patient_repo = CreatePatientRegisterPostgress()
        use_case = CreatePatientRegisterUseCase(create_patient_repo)

        # execute use case

        return {"message": "Create patient register route"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "something went wrong", "details": str(e)},
        )
