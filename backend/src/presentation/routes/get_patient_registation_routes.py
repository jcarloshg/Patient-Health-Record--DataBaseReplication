"""Get Patient Registration Route Module."""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.app.get_patient_registation.domain.criteria.criteria import CriteriaParser

# from src.app.get_patient_registation.application.get_patient_registation_use_case import (
#     GetPatientRegistationUseCase,
#     GetPatientRegistationProps
# )

get_patient_registation_route = APIRouter()


@get_patient_registation_route.get("/patient-register")
async def get_patient_registration(request: Request):
    """Route to get patient registration."""

    query_params = request.query_params
    query_params_primitives = query_params.__dict__.get('_dict')
    criteria_parser = CriteriaParser()
    criteria_parser.dict_to_criteria(query_params_primitives)

    # use_case = GetPatientRegistationUseCase()
    # props = GetPatientRegistationProps()
    # props['body'] = await request.json()

    # # execute use case
    # response = use_case.execute(props)
    # response_json = response.to_JSON_response()

    # return response
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "This is a placeholder response for patient registration."},
    )
