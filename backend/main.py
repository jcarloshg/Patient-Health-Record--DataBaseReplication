"""API v2 main module."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint of the API v2."""
    return "Hello, this is the main endpoint of the API v2"
