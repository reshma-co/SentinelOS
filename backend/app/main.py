from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
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


app = FastAPI(title="NitroStack API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# BASIC
# ----------------------------------------------------------------------


@app.get("/")
def read_root():
    return {"message": "NitroStack backend is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", service="nitrostack-backend")


# ----------------------------------------------------------------------
# VOLUNTEER
# ----------------------------------------------------------------------


@app.get("/volunteer")
def volunteer():
    agent = VolunteerAgent("volunteer-agent")
    result = agent.run("Flood response in Kochi")

    return {
        "agent": result.name,
        "status": "COMPLETED",
        "action": "Shelter team mobilized",
        "organization": "Volunteer Network",
        "description": result.output,
        "metric": "38",
        "metricLabel": "volunteers mobilized",
    }


# Frontend expects plural
@app.get("/volunteers")
def volunteers():
    return volunteer()


# ----------------------------------------------------------------------
# COMMUNICATION
# ----------------------------------------------------------------------


@app.get("/communication")
def communication():
    agent = CommunicationAgent("communication-agent")
    result = agent.run("Generate flood alert")

    return {
        "agent": result.name,
        "status": "COMPLETED",
        "action": "Emergency alert sent",
        "organization": "Emergency Communications",
        "description": result.output,
        "metric": "4",
        "metricLabel": "organizations notified",
    }


# Frontend expects plural
@app.get("/communications")
def communications():
    return communication()


# ----------------------------------------------------------------------
# WEATHER
# ----------------------------------------------------------------------


@app.get("/weather")
def weather():
    return {
        "agent": "Weather Agent",
        "status": "COMPLETED",
        "action": "Flood forecast confirmed",
        "organization": "Weather Department",
        "description": "180 mm rainfall recorded. Heavy rain expected.",
        "metric": "180 mm",
        "metricLabel": "rainfall recorded",
    }


# ----------------------------------------------------------------------
# HOSPITAL
# ----------------------------------------------------------------------


@app.get("/hospital")
def hospital():
    return {
        "agent": "Hospital Agent",
        "status": "COMPLETED",
        "action": "Medical capacity confirmed",
        "organization": "City Hospitals",
        "description": "Critical care capacity confirmed.",
        "metric": "12",
        "metricLabel": "beds available",
    }


# ----------------------------------------------------------------------
# POLICE
# ----------------------------------------------------------------------


@app.get("/police")
def police():
    return {
        "agent": "Police Agent",
        "status": "ALERT",
        "action": "Safe route validated",
        "organization": "Police Control",
        "description": "Flooded roads identified. Safe route available.",
        "metric": "1",
        "metricLabel": "safe route",
    }


# ----------------------------------------------------------------------
# TRANSPORT
# ----------------------------------------------------------------------


@app.get("/transport")
def transport():
    return {
        "agent": "Transport Agent",
        "status": "COMPLETED",
        "action": "Rescue fleet dispatched",
        "organization": "Transport Control",
        "description": "12 rescue boats dispatched.",
        "metric": "18 min",
        "metricLabel": "ETA",
    }


# ----------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------


@app.get("/mission/summary")
def mission_summary():
    return {
        "title": "Unified flood response plan",
        "items": [
            "Evacuate residents",
            "Deploy rescue boats",
            "Coordinate hospitals",
            "Send emergency alerts",
        ],
    }


# ----------------------------------------------------------------------
# REPORT
# ----------------------------------------------------------------------


@app.get("/mission/report")
def mission_report():
    return {
        "generatedAt": datetime.now().isoformat(),
        "status": "Mission Completed",
        "summary": "Unified emergency response generated successfully.",
    }


# ----------------------------------------------------------------------
# FRONTEND COMPATIBILITY
# ----------------------------------------------------------------------


@app.post("/mission/start")
async def mission_start():
    mission = CreateMissionInput(
        incident_description="Flood Emergency",
        location="Kochi, Kerala",
        severity="HIGH",
        timestamp=datetime.now().isoformat(),
    )

    result = await run_mission(mission)

    return {
        "id": getattr(result, "mission_id", "IN-26-0718"),
        "title": getattr(result, "title", "Flood Emergency"),
        "description": getattr(result, "summary", "Mission generated successfully."),
        "location": mission.location,
        "riskLevel": mission.severity,
        "agencies": 6,
        "coordinates": [9.9312, 76.2673],
        "raw": result
    }


# ----------------------------------------------------------------------
# ORIGINAL MISSION COMMANDER API
# ----------------------------------------------------------------------


@app.post("/mission", response_model=Mission)
def create_mission(mission_input: CreateMissionInput) -> Mission:
    return MissionService.create_mission(mission_input)


@app.post("/mission/{mission_id}/analyze", response_model=MissionContext)
def analyze_mission(mission_id: str) -> MissionContext:
    try:
        return IncidentAnalysisService.analyze_incident(mission_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/mission/{mission_id}/status")
def mission_status(mission_id: str):
    try:
        return get_mission_status(mission_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/mission/run", response_model=UnifiedMissionResponse)
async def run_mission_endpoint(
    mission_input: CreateMissionInput,
) -> UnifiedMissionResponse:
    return await run_mission(mission_input)
