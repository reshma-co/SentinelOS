"""Organizational modules invoked by Mission Commander.

PROJECT_CONTEXT.md lists WeatherModule/HospitalModule/PoliceModule/
TransportModule/VolunteerModule/CommunicationModule as PLANNED - NOT
IMPLEMENTED, and no such code exists anywhere in the canonical repository
that this environment has access to. Per the operator's explicit fallback
rule ("if a module is missing or broken, use a clearly marked fallback/mock
response so Mission Commander still completes the mission"), every handler
below is a deterministic MOCK implementation. status="mock_fallback" marks
this explicitly in every response so it is never confused with a live
integration. Swap a handler's body for a real API/service call later without
changing its signature.

Organization-specific logic lives here, not in Mission Commander (RULE 5).
"""
from __future__ import annotations

import asyncio

from .capability_registry import CAPABILITY_TO_MODULE
from .schemas import MissionContext, OrgResponse


def _capabilities_for_org(org: str, required_capabilities: list[str]) -> list[str]:
    return [
        cap for cap in required_capabilities
        if org in CAPABILITY_TO_MODULE.get(cap, [])
    ]


async def weather(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("weather", context.required_capabilities)
    return OrgResponse(
        organization="weather",
        status="mock_fallback",
        capabilities_covered=caps,
        summary=(
            f"Environmental conditions assessed for {context.incident_type} at "
            f"{context.location}; severity rated {context.severity}."
        ),
        recommendations=[
            "Issue environmental hazard advisory to affected zone",
            "Monitor conditions every 30 minutes for the mission duration",
        ],
        resources=["1 weather monitoring feed", "1 environmental risk bulletin"],
        raw={"mock": True, "hazards_considered": context.hazards},
    )


async def hospital(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("hospital", context.required_capabilities)
    severity_scale = {"critical": 6, "high": 4, "medium": 2, "low": 1, "unknown": 1}
    ambulances = severity_scale.get(context.severity, 1)
    return OrgResponse(
        organization="hospital",
        status="mock_fallback",
        capabilities_covered=caps,
        summary=(
            f"Medical response staged for {context.incident_type}; "
            f"{ambulances} ambulance unit(s) allocated based on {context.severity} severity."
        ),
        recommendations=[
            "Pre-position triage team near affected area",
            "Reserve emergency ward capacity",
        ],
        resources=[f"{ambulances} ambulance units", "1 mobile triage team"],
        raw={"mock": True, "ambulance_units": ambulances},
    )


async def police(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("police", context.required_capabilities)
    return OrgResponse(
        organization="police",
        status="mock_fallback",
        capabilities_covered=caps,
        summary=(
            f"Traffic control and perimeter security planned for {context.location}."
        ),
        recommendations=[
            "Close access roads within the affected perimeter",
            "Establish security checkpoint at evacuation routes",
        ],
        resources=["2 traffic control units", "1 perimeter security team"],
        raw={"mock": True},
    )


async def transport(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("transport", context.required_capabilities)
    routes = [
        f"Route A: fastest evacuation path out of {context.location}",
        f"Route B: alternate path avoiding {context.incident_type} hazard zone",
    ]
    return OrgResponse(
        organization="transport",
        status="mock_fallback",
        capabilities_covered=caps,
        summary=f"Road status checked and evacuation routes planned for {context.location}.",
        recommendations=[
            "Prioritize Route A unless blocked, then divert to Route B",
            "Stage rescue transport vehicles at rally point",
        ],
        resources=["3 rescue transport vehicles", "2 planned evacuation routes"],
        raw={"mock": True, "routes": routes},
    )


async def volunteer(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("volunteer", context.required_capabilities)
    return OrgResponse(
        organization="volunteer",
        status="mock_fallback",
        capabilities_covered=caps,
        summary="Shelter and relief distribution mobilized for affected population.",
        recommendations=[
            "Open nearest shelter and register displaced residents",
            "Distribute relief supplies at shelter intake point",
        ],
        resources=["1 shelter site", "20 volunteer personnel", "relief supply kits"],
        raw={"mock": True},
    )


async def communication(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("communication", context.required_capabilities)
    return OrgResponse(
        organization="communication",
        status="mock_fallback",
        capabilities_covered=caps,
        summary=f"Public alert drafted for {context.incident_type} at {context.location}.",
        recommendations=[
            "Broadcast public alert on all emergency channels",
            "Push periodic status updates every 15 minutes",
        ],
        resources=["1 emergency broadcast slot", "1 public alert SMS blast"],
        raw={"mock": True},
    )


ORGANIZATION_HANDLERS = {
    "weather": weather,
    "hospital": hospital,
    "police": police,
    "transport": transport,
    "volunteer": volunteer,
    "communication": communication,
}
