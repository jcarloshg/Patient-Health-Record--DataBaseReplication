"""Get Patient Registration Route Module."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.app.get_patient_registation.infra.persistence.slave_db.get_patient_postgress import GetPatientPostgress
from src.app.shared.domain.criteria.criteria import CriteriaParser
from src.app.get_patient_registation.application.get_patient_registation_use_case import (
    GetPatientRegistationUseCase,
    GetPatientRegistationProps
)

get_patient_registation_route = APIRouter()


@get_patient_registation_route.get("/patient-register")
async def get_patient_registration(request: Request):
    """Route to get patient registration."""

    # init data
    query_params = request.query_params
    query_params_primitives = query_params.__dict__.get('_dict')
    criteria_parser = CriteriaParser()
    criteria = criteria_parser.dict_to_criteria(query_params_primitives)

    #
    get_patient_postgress = GetPatientPostgress()

    # init use case props
    use_case = GetPatientRegistationUseCase(get_patient_postgress)
    props = GetPatientRegistationProps()
    props["criteria"] = criteria

    # execute use case
    response = use_case.execute(props)
    response_json = response.to_JSON_response()

    # return response
    return JSONResponse(
        status_code=response_json["status_code"],
        content=response_json["content"],
    )
