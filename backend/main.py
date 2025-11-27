"""API v2 main module."""

from fastapi import FastAPI

from src.presentation.routes.create_patient_register import create_patient_register_route
from src.presentation.routes.get_patient_registation_routes import get_patient_registation_route


app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint of the API v2."""
    return "Hello, this is the main endpoint of the API v2"


app.include_router(create_patient_register_route)
app.include_router(get_patient_registation_route)
