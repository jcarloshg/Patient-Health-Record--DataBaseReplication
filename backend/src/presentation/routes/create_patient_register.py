"""Module for create patient register route."""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
# domain
from src.app.create_patient_register.domain.events.event_bus import EventBus
from src.app.create_patient_register.domain.events.patient_register_created_event import PatientRegisterCreatedEvent
# infra
from src.app.create_patient_register.infra.persistence.main_db.create_patient_register_postgress import CreatePatientRegisterPostgress
from src.app.create_patient_register.infra.persistence.slave_db.replicate_patient_register_postgress import ReplicatePatientRegisterPostgress
# application
from src.app.create_patient_register.application.create_patient_register import CreatePatientRegisterProps, CreatePatientRegisterUseCase
from src.app.create_patient_register.application.domain_handlers.loggin_handler import LogginHandler
from src.app.create_patient_register.application.domain_handlers.persist_on_db_master import PersistOnDbMasterHandler
from src.app.create_patient_register.application.domain_handlers.replicate_record_on_slave import ReplicateRecordOnSlaveHandler


create_patient_register_route = APIRouter()


@create_patient_register_route.post("/patient-register")
async def create_patient_register(request: Request):
    """Route to create a patient register."""

   # init persistence
    create_patient_repo = CreatePatientRegisterPostgress()
    replicate_patient_repo = ReplicatePatientRegisterPostgress()

    # init event bus
    event_bus = EventBus()
    # init the event handlers
    logging_create_register_handler = LogginHandler(
        susbscribed_to=PatientRegisterCreatedEvent.event_name()
    )
    persist_on_db_master_handler = PersistOnDbMasterHandler(
        susbscribed_to=PatientRegisterCreatedEvent.event_name(),
        create_patient_repo=create_patient_repo
    )
    replicate_record_on_slave_handler = ReplicateRecordOnSlaveHandler(
        susbscribed_to=PatientRegisterCreatedEvent.event_name(),
        replicate_patient_repo=replicate_patient_repo
    )
    # subscribe the handlers to the event bus
    event_bus.subscribe(logging_create_register_handler)
    event_bus.subscribe(persist_on_db_master_handler)
    event_bus.subscribe(replicate_record_on_slave_handler)

    use_case = CreatePatientRegisterUseCase(event_bus=event_bus)
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
