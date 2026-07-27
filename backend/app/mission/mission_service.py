"""Phase 1: MissionService + IncidentAnalysisService.

Mirrors the duplicate-workspace contract documented in PROJECT_CONTEXT.md
section 3/5/6, migrated into the canonical repository.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from . import storage
from .capability_registry import classify_incident
from .schemas import CreateMissionInput, Mission, MissionContext


class MissionService:
    """Creates mission records from runtime input. No default incident."""

    @staticmethod
    def create_mission(mission_input: CreateMissionInput) -> Mission:
        mission_id = f"MSN-{uuid.uuid4().hex[:8]}"
        timestamp = mission_input.timestamp or datetime.now(timezone.utc).isoformat()
        mission = Mission(
            mission_id=mission_id,
            incident_description=mission_input.incident_description,
            location=mission_input.location,
            reported_severity=mission_input.severity,
            timestamp=timestamp,
            status="created",
        )
        storage.save(mission_id, mission=mission, mission_input=mission_input)
        return mission


class IncidentAnalysisService:
    """Deterministic keyword-based incident analysis. No live external data."""

    @staticmethod
    def analyze_incident(mission_id: str) -> MissionContext:
        record = storage.get(mission_id)
        if record is None:
            raise ValueError(f"Unknown mission_id: {mission_id}")
        mission_input: CreateMissionInput = record["mission_input"]
        context = classify_incident(mission_id, mission_input)
        storage.save(mission_id, context=context, status="analyzed")
        return context
