from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(title="NitroStack API", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "NitroStack backend is running"}


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="nitrostack-backend")
