"""API v2 main module."""

from fastapi import FastAPI

from src.presentation.routes.create_patient_register import create_patient_register_route

app = FastAPI()

app.include_router(create_patient_register_route)


@app.get("/")
def read_root():
    """Root endpoint of the API v2."""
    return "Hello, this is the main endpoint of the API v2"
