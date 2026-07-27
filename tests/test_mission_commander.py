import asyncio

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.mission import commander
from backend.app.mission.schemas import CreateMissionInput

client = TestClient(app)


def test_run_mission_flood_end_to_end():
    """Flood is only a test scenario here, not a hardcoded default."""
    payload = {
        "incident_description": "Severe flooding, dam break, rising fast near riverside colony",
        "location": "Riverside, Kerala",
    }
    response = client.post("/mission/run", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["emergency_type"] == "flood"
    assert body["severity"] == "critical"
    assert "hospital" in body["active_organizations"]
    assert "transport" in body["active_organizations"]
    assert len(body["organization_responses"]) == len(body["active_organizations"])
    assert body["priority_actions"]
    assert body["mission_timeline"]
    assert body["final_summary"]
    # not every incident activates every organization (RULE 7) —
    # a flood report has no keyword implying police perimeter security
    # beyond evacuation-driven routing, so this just checks shape, not identity.
    assert set(body["active_organizations"]) <= {
        "weather", "hospital", "police", "transport", "volunteer", "communication",
    }


def test_run_mission_does_not_default_to_flood():
    """A non-flood incident must never be classified as flood (RULE 1)."""
    payload = {
        "incident_description": "Building fire spreading fast, smoke visible from three blocks away",
        "location": "Sector 12 Industrial Area",
    }
    response = client.post("/mission/run", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["emergency_type"] == "fire"
    assert body["emergency_type"] != "flood"
    assert "hospital" in body["active_organizations"]
    assert "police" in body["active_organizations"]


def test_unknown_incident_handled_safely_not_flood():
    """RULE 8: unknown incidents must not default to any known scenario."""
    payload = {
        "incident_description": "Something strange happened at the warehouse",
        "location": "Unnamed Location",
    }
    response = client.post("/mission/run", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["emergency_type"] == "unknown"
    assert body["emergency_type"] != "flood"
    assert body["active_organizations"] == ["communication"]


def test_organization_failure_does_not_crash_mission():
    """Organizational failures must not crash the entire mission."""

    async def broken_hospital(context):
        raise RuntimeError("hospital API unreachable")

    mission_input = CreateMissionInput(
        incident_description="Road accident, multi-vehicle pile-up with casualties",
        location="Highway 47",
    )
    mission = commander.MissionService.create_mission(mission_input)
    context = commander.IncidentAnalysisService.analyze_incident(mission.mission_id)

    handlers = dict(commander.ORGANIZATION_HANDLERS)
    handlers["hospital"] = broken_hospital

    org_responses = asyncio.run(commander.dispatch_agents(context, handlers=handlers))

    hospital_response = next(r for r in org_responses if r.organization == "hospital")
    assert hospital_response.status == "error_fallback"
    # mission still produced responses for the other dispatched organizations
    assert len(org_responses) == len(commander.select_active_organizations(context))
    assert any(r.status == "mock_fallback" for r in org_responses)


def test_create_and_analyze_separately():
    create_resp = client.post(
        "/mission",
        json={"incident_description": "Cyclone approaching coast, category 4", "location": "Coastal Town"},
    )
    assert create_resp.status_code == 200
    mission_id = create_resp.json()["mission_id"]

    analyze_resp = client.post(f"/mission/{mission_id}/analyze")
    assert analyze_resp.status_code == 200
    context = analyze_resp.json()
    assert context["incident_type"] == "storm_cyclone"
    assert context["severity"] == "critical"

    status_resp = client.get(f"/mission/{mission_id}/status")
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "analyzed"


def test_missing_required_fields_rejected():
    response = client.post("/mission", json={"incident_description": "", "location": ""})
    assert response.status_code == 422
