"""Capability registry + incident -> capability classifier.

Architecture rule (PROJECT_CONTEXT.md RULE 1 / RULE 4 / RULE 8):
Mission Commander must stay scenario-agnostic. There is NO default incident
type. Flood is one recognized incident pattern among several — it has no
special status in this module and is not returned for unmatched input.
Unmatched/unknown input is classified as "unknown" with a minimal, safe
capability set instead of collapsing to any specific known scenario.
"""
from __future__ import annotations

from dataclasses import dataclass

from .schemas import CreateMissionInput, MissionContext

# --- Capability registry (PROJECT_CONTEXT.md section 7) ----------------

CAPABILITY_TO_MODULE: dict[str, list[str]] = {
    "weather_conditions": ["weather"],
    "environmental_risk": ["weather"],
    "emergency_medical_response": ["hospital"],
    "ambulance_support": ["hospital"],
    "evacuation": ["police", "transport", "volunteer"],
    "traffic_control": ["police"],
    "perimeter_security": ["police"],
    "road_status": ["transport"],
    "route_planning": ["transport"],
    "rescue_transport": ["transport"],
    "logistics": ["transport", "volunteer"],
    "shelter_support": ["volunteer"],
    "relief_distribution": ["volunteer"],
    "manpower": ["volunteer"],
    "public_alert": ["communication"],
    "emergency_broadcast": ["communication"],
}

ALL_CAPABILITIES: set[str] = set(CAPABILITY_TO_MODULE)


@dataclass(frozen=True)
class IncidentPattern:
    incident_type: str
    keywords: tuple[str, ...]
    hazards: tuple[str, ...]
    capabilities: tuple[str, ...]
    high_severity_keywords: tuple[str, ...] = ()


# Generic incident patterns. Order does not imply priority/default — every
# incoming description is scored against all patterns and the best match
# wins. Flood is just one entry among many, not a fallback.
INCIDENT_PATTERNS: tuple[IncidentPattern, ...] = (
    IncidentPattern(
        incident_type="flood",
        keywords=("flood", "flooding", "inundat", "waterlogg", "overflow", "dam break", "river burst"),
        hazards=("rising water", "contaminated water", "drowning risk", "waterborne disease"),
        capabilities=(
            "weather_conditions", "environmental_risk", "evacuation", "rescue_transport",
            "shelter_support", "relief_distribution", "public_alert", "emergency_medical_response",
        ),
        high_severity_keywords=("dam break", "flash flood", "trapped", "rising fast"),
    ),
    IncidentPattern(
        incident_type="fire",
        keywords=("fire", "blaze", "wildfire", "burning", "smoke"),
        hazards=("smoke inhalation", "structural collapse", "rapid spread"),
        capabilities=(
            "environmental_risk", "evacuation", "traffic_control", "perimeter_security",
            "emergency_medical_response", "ambulance_support", "public_alert", "logistics",
        ),
        high_severity_keywords=("spreading fast", "explosion", "trapped", "high-rise"),
    ),
    IncidentPattern(
        incident_type="earthquake",
        keywords=("earthquake", "tremor", "seismic", "quake"),
        hazards=("structural collapse", "aftershocks", "gas leaks"),
        capabilities=(
            "environmental_risk", "evacuation", "rescue_transport", "emergency_medical_response",
            "ambulance_support", "shelter_support", "manpower", "public_alert", "perimeter_security",
        ),
        high_severity_keywords=("collapse", "trapped", "mass casualty"),
    ),
    IncidentPattern(
        incident_type="storm_cyclone",
        keywords=("cyclone", "hurricane", "storm", "typhoon", "high wind"),
        hazards=("wind damage", "power outage", "flying debris"),
        capabilities=(
            "weather_conditions", "environmental_risk", "evacuation", "shelter_support",
            "public_alert", "emergency_broadcast", "logistics",
        ),
        high_severity_keywords=("category 4", "category 5", "landfall imminent"),
    ),
    IncidentPattern(
        incident_type="road_accident",
        keywords=("accident", "collision", "crash", "pile-up", "pile up"),
        hazards=("traffic obstruction", "fuel spill", "casualties"),
        capabilities=(
            "traffic_control", "emergency_medical_response", "ambulance_support",
            "road_status", "route_planning",
        ),
        high_severity_keywords=("multi-vehicle", "mass casualty", "fatalities"),
    ),
    IncidentPattern(
        incident_type="medical_emergency",
        keywords=("outbreak", "epidemic", "mass casualty", "poisoning", "medical emergency"),
        hazards=("disease spread", "overwhelmed medical capacity"),
        capabilities=(
            "emergency_medical_response", "ambulance_support", "public_alert",
            "logistics", "manpower",
        ),
        high_severity_keywords=("outbreak", "epidemic", "mass casualty"),
    ),
    IncidentPattern(
        incident_type="hazmat_industrial",
        keywords=("chemical leak", "gas leak", "hazmat", "toxic spill", "explosion"),
        hazards=("toxic exposure", "explosion risk", "contamination"),
        capabilities=(
            "environmental_risk", "evacuation", "perimeter_security", "emergency_medical_response",
            "ambulance_support", "public_alert",
        ),
        high_severity_keywords=("explosion", "mass exposure", "toxic cloud"),
    ),
    IncidentPattern(
        incident_type="power_outage",
        keywords=("power outage", "blackout", "grid failure", "transformer failure", "electrical outage"),
        hazards=("loss of power", "traffic signal failure", "communications disruption"),
        capabilities=(
            "environmental_risk", "traffic_control", "road_status", "route_planning",
            "emergency_medical_response", "logistics", "manpower", "public_alert",
            "emergency_broadcast",
        ),
        high_severity_keywords=("citywide", "hospital outage", "grid failure", "critical infrastructure"),
    ),
)

SEVERITY_LEVELS = ("low", "medium", "high", "critical", "unknown")


def _normalize_severity(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized if normalized in SEVERITY_LEVELS else None


def classify_incident(mission_id: str, mission_input: CreateMissionInput) -> MissionContext:
    """Deterministic keyword-based classifier. No live external data.

    Scores every known pattern against the description and picks the best
    match. If nothing matches meaningfully, returns incident_type="unknown"
    with a minimal, safe capability set — it never falls back to a specific
    known scenario (RULE 8).
    """
    text = mission_input.incident_description.lower()

    best_pattern: IncidentPattern | None = None
    best_score = 0
    for pattern in INCIDENT_PATTERNS:
        score = sum(1 for kw in pattern.keywords if kw in text)
        if score > best_score:
            best_score = score
            best_pattern = pattern

    reported_severity = _normalize_severity(mission_input.severity)

    if best_pattern is None or best_score == 0:
        # Genuinely unknown incident — safe minimal response, not a default scenario.
        return MissionContext(
            mission_id=mission_id,
            incident_type="unknown",
            location=mission_input.location,
            severity=reported_severity or "unknown",
            hazards=[],
            required_capabilities=["public_alert"],
            status="analyzed",
        )

    if reported_severity:
        severity = reported_severity
    elif any(kw in text for kw in best_pattern.high_severity_keywords):
        severity = "critical"
    elif best_score >= 2:
        severity = "high"
    else:
        severity = "medium"

    return MissionContext(
        mission_id=mission_id,
        incident_type=best_pattern.incident_type,
        location=mission_input.location,
        severity=severity,
        hazards=list(best_pattern.hazards),
        required_capabilities=list(best_pattern.capabilities),
        status="analyzed",
    )


def capabilities_to_organizations(capabilities: list[str]) -> list[str]:
    """Capability -> module routing (RULE: capability-based, not incident-based)."""
    orgs: list[str] = []
    for capability in capabilities:
        for org in CAPABILITY_TO_MODULE.get(capability, []):
            if org not in orgs:
                orgs.append(org)
    return orgs
