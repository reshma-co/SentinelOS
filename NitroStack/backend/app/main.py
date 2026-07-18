from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.communication_agent import CommunicationAgent
from agents.volunteer_agent import VolunteerAgent

from .mission.commander import get_mission_status, run_mission
from .mission.mission_service import IncidentAnalysisService, MissionService
from .mission.organizations import ORGANIZATION_HANDLERS
from .mission.schemas import (
    CreateMissionInput,
    Mission,
    MissionContext,
    OrgResponse,
    UnifiedMissionResponse,
)

logger = logging.getLogger("nitrostack.api")


class HealthResponse(BaseModel):
    status: str
    service: str


class StartMissionRequest(BaseModel):
    scenario: str | None = None


SCENARIOS: dict[str, dict[str, Any]] = {
    "flood": {
        "name": "Flood Emergency",
        "title": "Monsoon flooding: response in motion",
        "description": "Severe flooding, dam break, rising fast near riverside colony",
        "location": "Kochi, Kerala",
        "severity": "HIGH",
        "coordinates": [9.9312, 76.2673],
    },
    "earthquake": {
        "name": "Earthquake Response",
        "title": "Urban earthquake response",
        "description": "Earthquake tremor with possible building collapse and trapped residents",
        "location": "Guwahati, Assam",
        "severity": "CRITICAL",
        "coordinates": [26.1445, 91.7362],
    },
    "chemical": {
        "name": "Chemical Leak",
        "title": "Industrial chemical leak containment",
        "description": "Chemical leak with toxic cloud risk near industrial storage tanks",
        "location": "Visakhapatnam, Andhra Pradesh",
        "severity": "HIGH",
        "coordinates": [17.6868, 83.2185],
    },
    "power": {
        "name": "Power Outage",
        "title": "Citywide power outage response",
        "description": "Citywide power outage after grid failure affecting traffic and hospitals",
        "location": "Bengaluru, Karnataka",
        "severity": "HIGH",
        "coordinates": [12.9716, 77.5946],
    },
}

AGENT_LABELS = {
    "weather": "Weather Agent",
    "hospital": "Hospital Agent",
    "police": "Police Agent",
    "transport": "Transport Agent",
    "volunteer": "Volunteer Agent",
    "communication": "Comms Agent",
}

ENDPOINT_TO_ORG = {
    "weather": "weather",
    "hospital": "hospital",
    "police": "police",
    "transport": "transport",
    "volunteers": "volunteer",
    "communications": "communication",
}

LAST_STATE: dict[str, Any] = {
    "scenario": "flood",
    "mission": None,
    "adapted": None,
    "agents": {},
    "started_at": None,
}

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


def _scenario_key(value: str | None) -> str:
    key = (value or LAST_STATE.get("scenario") or "flood").strip().lower()
    return key if key in SCENARIOS else "flood"


def _mission_input_for(scenario_key: str) -> CreateMissionInput:
    scenario = SCENARIOS[scenario_key]
    return CreateMissionInput(
        incident_description=scenario["description"],
        location=scenario["location"],
        severity=scenario["severity"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def _mission_context_for(scenario_key: str) -> MissionContext:
    mission = MissionService.create_mission(_mission_input_for(scenario_key))
    return IncidentAnalysisService.analyze_incident(mission.mission_id)


def _response_dump(response: UnifiedMissionResponse) -> dict[str, Any]:
    return response.model_dump(mode="json")


def adapt_mission_response(
    response: UnifiedMissionResponse,
    scenario_key: str,
) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_key]
    agencies = len(response.active_organizations) or len(ENDPOINT_TO_ORG)
    return {
        "id": response.mission_id,
        "title": scenario["title"],
        "description": response.final_summary or scenario["description"],
        "location": response.location or scenario["location"],
        "riskLevel": (response.severity or scenario["severity"]).upper(),
        "agencies": agencies,
        "coordinates": scenario["coordinates"],
        "scenario": scenario_key,
        "aiOutput": _response_dump(response),
    }


def _fallback_agent_response(org: str, scenario_key: str, reason: str) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_key]
    return {
        "agent": AGENT_LABELS.get(org, f"{org.title()} Agent"),
        "icon": "o",
        "status": "DEGRADED",
        "action": f"{org.title()} fallback activated",
        "organization": org.title(),
        "description": f"Automated {org} response unavailable for {scenario['name']}; manual coordination required. {reason}",
        "metric": "Manual",
        "metricLabel": "verification required",
    }


def _agent_response_from_org(org: str, response: OrgResponse, scenario_key: str) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_key]
    resources = response.resources or []
    recommendations = response.recommendations or []
    first_resource = resources[0] if resources else "Ready"
    status = "COMPLETED" if response.status in {"ok", "mock_fallback"} else "DEGRADED"
    body = {
        "agent": AGENT_LABELS.get(org, f"{org.title()} Agent"),
        "icon": "o",
        "status": status,
        "action": recommendations[0] if recommendations else f"{org.title()} response generated",
        "organization": org.title(),
        "description": response.summary,
        "metric": str(first_resource).split(" ", 1)[0],
        "metricLabel": str(first_resource).split(" ", 1)[1] if " " in str(first_resource) else "resource",
        "recommendations": recommendations,
        "resources": resources,
        "raw": response.raw,
    }
    if org == "weather":
        body["mapMarkers"] = [{"type": "incident", "label": f"{scenario['name']} incident", "coordinates": scenario["coordinates"]}]
    if org == "hospital":
        body["mapMarkers"] = [{"type": "hospital", "label": "Emergency hospital capacity", "coordinates": [scenario["coordinates"][0] + 0.02, scenario["coordinates"][1] + 0.02]}]
    if org == "transport":
        body["route"] = [
            scenario["coordinates"],
            [scenario["coordinates"][0] + 0.012, scenario["coordinates"][1] - 0.012],
            [scenario["coordinates"][0] + 0.022, scenario["coordinates"][1] - 0.02],
        ]
    return body


async def _run_org_endpoint(endpoint_key: str, scenario: str | None = None) -> dict[str, Any]:
    scenario_key = _scenario_key(scenario)
    org = ENDPOINT_TO_ORG[endpoint_key]
    try:
        if org == "volunteer":
            result = VolunteerAgent("volunteer-agent").run(f"{SCENARIOS[scenario_key]['name']} at {SCENARIOS[scenario_key]['location']}")
            output = json.loads(result.output)
            count = output.get("total_available_volunteers", len(output.get("available_volunteers", [])))
            shelters = output.get("available_shelters", [])
            body = {
                "agent": result.name,
                "icon": "o",
                "status": "COMPLETED",
                "action": "Shelter team mobilized",
                "organization": "Volunteer Network",
                "description": f"{count} volunteers available; {len(shelters)} shelter site(s) open for {SCENARIOS[scenario_key]['name']}.",
                "metric": str(count),
                "metricLabel": "volunteers available",
                "mapMarkers": [{"type": "shelter", "label": shelters[0]["name"], "coordinates": SCENARIOS[scenario_key]["coordinates"]}] if shelters else [],
                "raw": output,
            }
        elif org == "communication":
            result = CommunicationAgent("communication-agent").run(f"{SCENARIOS[scenario_key]['name']} at {SCENARIOS[scenario_key]['location']}")
            body = {
                "agent": result.name,
                "icon": "o",
                "status": "COMPLETED",
                "action": "Emergency alert generated",
                "organization": "Emergency Communications",
                "description": result.output,
                "metric": "6",
                "metricLabel": "channels prepared",
                "recipients": ["Police", "Hospitals", "Transport", "Volunteer Network", "Public Alert", "Mission Commander"],
            }
        else:
            handler = ORGANIZATION_HANDLERS[org]
            body = _agent_response_from_org(org, await handler(_mission_context_for(scenario_key)), scenario_key)
        LAST_STATE["agents"][endpoint_key] = body
        return body
    except Exception as exc:  # noqa: BLE001
        logger.exception("Agent endpoint failed: %s", endpoint_key)
        body = _fallback_agent_response(org, scenario_key, type(exc).__name__)
        LAST_STATE["agents"][endpoint_key] = body
        return body


def _summary_from_state() -> dict[str, Any]:
    adapted = LAST_STATE.get("adapted") or adapt_mission_response(
        UnifiedMissionResponse(
            mission_id="preview",
            emergency_type="unknown",
            location=SCENARIOS[_scenario_key(None)]["location"],
            status="preview",
            severity=SCENARIOS[_scenario_key(None)]["severity"].lower(),
            active_organizations=list(ENDPOINT_TO_ORG.values()),
            organization_responses=[],
            priority_actions=[],
            resource_allocation=[],
            evacuation_routes=[],
            communication_plan=[],
            mission_timeline=[],
            final_summary=SCENARIOS[_scenario_key(None)]["description"],
        ),
        _scenario_key(None),
    )
    ai_output = adapted.get("aiOutput", {})
    actions = ai_output.get("priority_actions") or []
    agent_items = [
        f"{value.get('organization', key)}: {value.get('action', 'response ready')}"
        for key, value in LAST_STATE.get("agents", {}).items()
    ]
    items = (actions[:3] + agent_items[:3]) or [adapted["description"]]
    return {"title": f"Unified {SCENARIOS[_scenario_key(None)]['name'].lower()} plan", "items": items}


def _report_from_state() -> dict[str, Any]:
    adapted = LAST_STATE.get("adapted")
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "Mission Completed" if adapted else "Mission Pending",
        "mission": adapted or {},
        "participatingOrganizations": list((adapted or {}).get("aiOutput", {}).get("active_organizations", [])),
        "agentOutputs": LAST_STATE.get("agents", {}),
        "summary": _summary_from_state(),
        "recommendedActions": (adapted or {}).get("aiOutput", {}).get("priority_actions", []),
        "timestamps": {
            "startedAt": LAST_STATE.get("started_at"),
            "reportedAt": datetime.now(timezone.utc).isoformat(),
        },
    }


@app.get("/")
def read_root():
    return {"message": "NitroStack backend is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", service="nitrostack-backend")


@app.get("/volunteer")
async def volunteer(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("volunteers", scenario)


@app.get("/volunteers")
async def volunteers(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("volunteers", scenario)


@app.get("/communication")
async def communication(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("communications", scenario)


@app.get("/communications")
async def communications(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("communications", scenario)


@app.get("/weather")
async def weather(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("weather", scenario)


@app.get("/hospital")
async def hospital(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("hospital", scenario)


@app.get("/police")
async def police(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("police", scenario)


@app.get("/transport")
async def transport(scenario: str | None = Query(default=None)):
    return await _run_org_endpoint("transport", scenario)


@app.get("/mission/summary")
def mission_summary():
    return _summary_from_state()


@app.get("/mission/report")
def mission_report():
    return _report_from_state()


@app.post("/mission/start")
async def mission_start(request: StartMissionRequest | None = None):
    scenario_key = _scenario_key(request.scenario if request else None)
    try:
        response = await run_mission(_mission_input_for(scenario_key))
        adapted = adapt_mission_response(response, scenario_key)
        LAST_STATE.update(
            {
                "scenario": scenario_key,
                "mission": response,
                "adapted": adapted,
                "agents": {},
                "started_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        return adapted
    except Exception as exc:  # noqa: BLE001
        logger.exception("Mission start failed")
        fallback = {
            "id": f"fallback-{datetime.now(timezone.utc).strftime('%H%M%S')}",
            "title": SCENARIOS[scenario_key]["title"],
            "description": f"Mission Commander is temporarily degraded ({type(exc).__name__}); fallback coordination is active.",
            "location": SCENARIOS[scenario_key]["location"],
            "riskLevel": SCENARIOS[scenario_key]["severity"],
            "agencies": len(ENDPOINT_TO_ORG),
            "coordinates": SCENARIOS[scenario_key]["coordinates"],
            "scenario": scenario_key,
            "aiOutput": {"status": "fallback", "error": type(exc).__name__},
        }
        LAST_STATE.update({"scenario": scenario_key, "adapted": fallback, "agents": {}})
        return fallback


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
    try:
        return await run_mission(mission_input)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Mission run failed")
        raise HTTPException(
            status_code=503,
            detail={"message": "Mission Commander unavailable", "error": type(exc).__name__},
        ) from exc
