# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.mission import router as mission_router
from app.utils.logger import logger

app = FastAPI(
    title="SentinelOS API",
    version="1.0.0",
    description="Unified Emergency Coordination Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(mission_router)

logger.info("SentinelOS API initialized successfully.")
