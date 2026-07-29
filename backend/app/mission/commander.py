"""Mission Commander: Phases 2-6.

Mission Commander coordinates capabilities and structured outputs; it does
NOT contain organization-specific logic (RULE 5/6) and does NOT hardcode any
incident type as a default (RULE 1/4). It also never activates every
organization for every incident (RULE 7) — only the organizations implied
by the classified required_capabilities are dispatched.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

import asyncio

from . import storage
from .capability_registry import capabilities_to_organizations
from .mission_service import IncidentAnalysisService, MissionService
from .organizations import ORGANIZATION_HANDLERS
from .schemas import (
    CreateMissionInput,
    Mission,
    MissionContext,
    OrgResponse,
    TimelineStep,
    UnifiedMissionResponse,
)

OrgHandler = Callable[[MissionContext], Awaitable[OrgResponse]]


async def _safe_call(
    org: str, handler: OrgHandler, context: MissionContext
) -> OrgResponse:
    """Wrap an organization call so one failure never crashes the mission (rule: organizational failures must not crash the mission)."""
    try:
        return await handler(context)
    except Exception as exc:  # noqa: BLE001 - deliberately broad: any org failure must degrade gracefully
        return OrgResponse(
            organization=org,
            status="error_fallback",
            capabilities_covered=[],
            summary=f"{org} module failed to respond ({type(exc).__name__}); using safe fallback so the mission can proceed.",
            recommendations=[
                f"Manually verify {org} status — automated response unavailable"
            ],
            resources=[],
            raw={"error": str(exc)},
        )


def select_active_organizations(context: MissionContext) -> list[str]:
    """Capability -> organization routing. Only routes orgs actually implied by capabilities."""
    return capabilities_to_organizations(context.required_capabilities)


async def dispatch_agents(
    context: MissionContext,
    handlers: dict[str, OrgHandler] | None = None,
) -> list[OrgResponse]:
    """Phase 2: invoke relevant organizational modules concurrently."""
    handlers = handlers or ORGANIZATION_HANDLERS
    active_orgs = select_active_organizations(context)
    tasks = [
        _safe_call(org, handlers[org], context)
        for org in active_orgs
        if org in handlers
    ]
    if not tasks:
        return []
    return list(await asyncio.gather(*tasks))


def prioritize_actions(
    context: MissionContext, org_responses: list[OrgResponse]
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Phase 3 (part of execute_coordination): aggregate + prioritize outputs."""
    priority_actions: list[str] = []
    resource_allocation: list[str] = []
    evacuation_routes: list[str] = []
    communication_plan: list[str] = []

    # Severity-critical incidents surface medical/evacuation actions first.
    ordered = org_responses
    if context.severity in ("critical", "high"):
        weight = {"hospital": 0, "transport": 1, "police": 2}
        ordered = sorted(org_responses, key=lambda r: weight.get(r.organization, 5))

    for response in ordered:
        priority_actions.extend(response.recommendations)
        resource_allocation.extend(response.resources)
        if response.organization == "transport":
            evacuation_routes.extend(response.raw.get("routes", []))
        if response.organization == "communication":
            communication_plan.extend(response.recommendations)

    if not communication_plan:
        communication_plan.append(
            "No communication module dispatched for this incident classification; "
            "public alert not required by current capability set."
        )

    return priority_actions, resource_allocation, evacuation_routes, communication_plan


def generate_mission_plan(
    context: MissionContext, org_responses: list[OrgResponse]
) -> list[TimelineStep]:
    """Phase 4: build the mission timeline."""
    steps: list[TimelineStep] = [
        TimelineStep(
            step=1,
            phase="report",
            description="Incident reported and mission created.",
            eta_minutes=0,
        ),
        TimelineStep(
            step=2,
            phase="analysis",
            description=f"Incident classified as '{context.incident_type}' (severity: {context.severity}).",
            eta_minutes=1,
        ),
        TimelineStep(
            step=3,
            phase="dispatch",
            description=f"Dispatched {len(org_responses)} organization(s): "
            f"{', '.join(r.organization for r in org_responses) or 'none'}.",
            eta_minutes=3,
        ),
    ]
    eta = 5
    for response in org_responses:
        steps.append(
            TimelineStep(
                step=len(steps) + 1,
                phase=f"{response.organization}_response",
                description=response.summary,
                eta_minutes=eta,
            )
        )
        eta += 5
    steps.append(
        TimelineStep(
            step=len(steps) + 1,
            phase="coordination",
            description="Mission Commander prioritized actions and finalized unified mission plan.",
            eta_minutes=eta,
        )
    )
    return steps


def get_mission_status(mission_id: str) -> dict:
    """Phase 5: get_mission_status."""
    record = storage.get(mission_id)
    if record is None:
        raise ValueError(f"Unknown mission_id: {mission_id}")
    return {
        "mission_id": mission_id,
        "status": record.get("status", "unknown"),
        "has_context": "context" in record,
        "has_unified_response": "unified_response" in record,
    }


async def run_mission(mission_input: CreateMissionInput) -> UnifiedMissionResponse:
    """End-to-end Mission Commander flow (Phases 1-6) — the primary entry point."""
    mission: Mission = MissionService.create_mission(mission_input)
    context: MissionContext = IncidentAnalysisService.analyze_incident(
        mission.mission_id
    )

    org_responses = await dispatch_agents(context)
    active_orgs = [r.organization for r in org_responses]

    priority_actions, resource_allocation, evacuation_routes, communication_plan = (
        prioritize_actions(context, org_responses)
    )
    timeline = generate_mission_plan(context, org_responses)

    failed = [r for r in org_responses if r.status == "error_fallback"]
    if org_responses and len(failed) == len(org_responses):
        status = "completed_with_errors"
    else:
        status = "completed"

    top_actions = priority_actions[:2]
    final_summary = (
        f"Mission {mission.mission_id}: '{context.incident_type}' incident at {context.location} "
        f"(severity: {context.severity}). {len(active_orgs)} organization(s) coordinated "
        f"({', '.join(active_orgs) or 'none'}). "
        f"Top priority actions: {'; '.join(top_actions) if top_actions else 'none identified'}."
    )

    response = UnifiedMissionResponse(
        mission_id=mission.mission_id,
        emergency_type=context.incident_type,
        location=context.location,
        status=status,
        severity=context.severity,
        active_organizations=active_orgs,
        organization_responses=org_responses,
        priority_actions=priority_actions,
        resource_allocation=resource_allocation,
        evacuation_routes=evacuation_routes,
        communication_plan=communication_plan,
        mission_timeline=timeline,
        final_summary=final_summary,
    )
    storage.save(mission.mission_id, status=status, unified_response=response)
    return response
