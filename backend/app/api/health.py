from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/")
def root():
    return {"message": "SentinelOS backend is running"}


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        service="sentinelos-backend",
    )
