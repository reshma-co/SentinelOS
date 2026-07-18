from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.volunteer_agent import VolunteerAgent
from agents.communication_agent import CommunicationAgent

from .mission.commander import get_mission_status, run_mission
from .mission.mission_service import IncidentAnalysisService, MissionService
from .mission.schemas import (
    CreateMissionInput,
    Mission,
    MissionContext,
    UnifiedMissionResponse,
)


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(
    title="NitroStack API",
    version="0.1.0"
)


@app.get("/")
def read_root():
    return {"message": "NitroStack backend is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        service="nitrostack-backend"
    )


# --- Volunteer Agent -----------------------------------------------------

@app.get("/volunteer")
def volunteer():
    agent = VolunteerAgent("volunteer-agent")
    result = agent.run("Flood response in Kochi")
    return {
        "agent": result.name,
        "output": result.output
    }


# --- Communication Agent ------------------------------------------------

@app.get("/communication")
def communication():
    agent = CommunicationAgent("communication-agent")
    result = agent.run("Generate flood alert")
    return {
        "agent": result.name,
        "output": result.output
    }


# --- Mission Commander ---------------------------------------------------

@app.post("/mission", response_model=Mission)
def create_mission(mission_input: CreateMissionInput) -> Mission:
    """Create a mission record from runtime input."""
    return MissionService.create_mission(mission_input)


@app.post("/mission/{mission_id}/analyze", response_model=MissionContext)
def analyze_mission(mission_id: str) -> MissionContext:
    """Analyze a previously created mission's incident."""
    try:
        return IncidentAnalysisService.analyze_incident(mission_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/mission/{mission_id}/status")
def mission_status(mission_id: str) -> dict:
    """Get the current mission status."""
    try:
        return get_mission_status(mission_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/mission/run", response_model=UnifiedMissionResponse)
async def run_mission_endpoint(
    mission_input: CreateMissionInput,
) -> UnifiedMissionResponse:
    """Run the complete Mission Commander workflow."""
    return await run_mission(mission_input)