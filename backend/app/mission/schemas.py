"""Pydantic schemas for the Mission Commander protocol.

Schemas mirror the contracts recorded in PROJECT_CONTEXT.md section 5/6/7.
No incident type is treated as a default anywhere in this module.
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class CreateMissionInput(BaseModel):
    """Canonical runtime mission input (PROJECT_CONTEXT.md section 5)."""

    incident_description: str
    location: str
    severity: Optional[str] = None
    timestamp: Optional[str] = None

    @field_validator("incident_description", "location")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must be a non-empty string")
        return stripped

    @field_validator("severity", "timestamp")
    @classmethod
    def _optional_trim_to_none(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class Mission(BaseModel):
    """Raw mission record as originally reported (Phase 1: create_mission)."""

    mission_id: str
    incident_description: str
    location: str
    reported_severity: Optional[str] = None
    timestamp: str
    status: str = "created"


class MissionContext(BaseModel):
    """Analyzed operational context (Phase 1: analyze_incident)."""

    mission_id: str
    incident_type: str
    location: str
    severity: str  # low | medium | high | critical | unknown
    hazards: list[str] = Field(default_factory=list)
    required_capabilities: list[str] = Field(default_factory=list)
    status: str = "analyzed"


class OrgResponse(BaseModel):
    """Structured response from one organizational module/tool."""

    organization: str
    status: str  # ok | mock_fallback | error_fallback
    capabilities_covered: list[str] = Field(default_factory=list)
    summary: str
    recommendations: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


class TimelineStep(BaseModel):
    step: int
    phase: str
    description: str
    eta_minutes: int


class UnifiedMissionResponse(BaseModel):
    """Final Mission Commander output — the contract requested by the user."""

    mission_id: str
    emergency_type: str
    location: str
    status: str
    severity: str
    active_organizations: list[str]
    organization_responses: list[OrgResponse]
    priority_actions: list[str]
    resource_allocation: list[str]
    evacuation_routes: list[str]
    communication_plan: list[str]
    mission_timeline: list[TimelineStep]
    final_summary: str
