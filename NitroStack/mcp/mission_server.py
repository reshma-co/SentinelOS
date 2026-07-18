"""Mission Commander MCP server.

Follows the same FastMCP convention as sample_server.py (RULE 11: reuse
existing patterns, don't invent unsupported decorators/APIs). Kept as a
separate server so sample_server.py / the echo tool are untouched
(preserve teammate work).

Run standalone:
    python mission_server.py

Or via the sample client pattern using StdioServerParameters(args=["mission_server.py"]).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Reuse the mission logic living in backend/app/mission instead of duplicating it.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from mcp.server.fastmcp import FastMCP

from app.mission.commander import get_mission_status as _get_mission_status
from app.mission.commander import run_mission as _run_mission
from app.mission.mission_service import IncidentAnalysisService, MissionService
from app.mission.schemas import CreateMissionInput

mcp = FastMCP("sentinelos-mission-commander")


@mcp.tool()
def create_mission(incident_description: str, location: str, severity: str | None = None, timestamp: str | None = None) -> dict:
    """Phase 1: create a mission record from runtime input. No default incident."""
    mission_input = CreateMissionInput(
        incident_description=incident_description,
        location=location,
        severity=severity,
        timestamp=timestamp,
    )
    return MissionService.create_mission(mission_input).model_dump()


@mcp.tool()
def analyze_incident(mission_id: str) -> dict:
    """Phase 1: classify a previously created mission's incident."""
    return IncidentAnalysisService.analyze_incident(mission_id).model_dump()


@mcp.tool()
def get_mission_status(mission_id: str) -> dict:
    """Phase 5: get current mission status."""
    return _get_mission_status(mission_id)


@mcp.tool()
async def run_mission(incident_description: str, location: str, severity: str | None = None, timestamp: str | None = None) -> dict:
    """End-to-end Mission Commander flow: create -> analyze -> dispatch_agents ->
    execute_coordination -> generate_mission_plan -> unified mission response.
    Scenario-agnostic: incident_description/location must be supplied at runtime."""
    mission_input = CreateMissionInput(
        incident_description=incident_description,
        location=location,
        severity=severity,
        timestamp=timestamp,
    )
    result = await _run_mission(mission_input)
    return result.model_dump()


@mcp.resource("nitrostack://mission-commander/status")
def mission_commander_status() -> str:
    return "SentinelOS Mission Commander MCP server is ready."


if __name__ == "__main__":
    mcp.run()
