from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .services import HospitalService

hospital_service = HospitalService()


def register_hospital_module(mcp: FastMCP) -> None:

    @mcp.tool(
        description="Find hospitals near a location with matching emergency capability and bed availability."
    )
    def find_hospital(
        location: str,
        emergency_type: str | None = None,
        radius_km: float = 10,
    ) -> dict:

        if not location.strip():
            raise ValueError("location is required")

        return hospital_service.find_hospital(
            location.strip(),
            emergency_type,
            radius_km,
        )

    @mcp.tool(
        description="Check ICU capacity for a hospital by ID or exact hospital name."
    )
    def check_icu(hospital_id_or_name: str) -> dict:

        if not hospital_id_or_name.strip():
            raise ValueError("hospital_id_or_name is required")

        return hospital_service.check_icu(
            hospital_id_or_name.strip()
        )

    @mcp.tool(
        description="Find available ambulances near an emergency location."
    )
    def find_ambulance(
        location: str,
        radius_km: float = 10,
    ) -> dict:

        if not location.strip():
            raise ValueError("location is required")

        return hospital_service.find_ambulance(
            location.strip(),
            radius_km,
        )

    @mcp.tool(
        description="Allocate a medical response team for an incident."
    )
    def allocate_medical_team(
        incident_location: str,
        emergency_severity: str,
        required_specialization: str | None = None,
    ) -> dict:

        if not incident_location.strip():
            raise ValueError("incident_location is required")

        return hospital_service.allocate_medical_team(
            incident_location.strip(),
            emergency_severity,
            required_specialization,
        )

    @mcp.resource(
        "sentinel://hospital/database",
        name="hospital_database",
        mime_type="application/json",
    )
    def hospital_database() -> dict:
        return {
            "hospital_database":
            hospital_service.resources()["hospital_database"]
        }

    @mcp.resource(
        "sentinel://hospital/ambulances",
        name="ambulance_locations",
        mime_type="application/json",
    )
    def ambulance_locations() -> dict:
        return {
            "ambulance_locations":
            hospital_service.resources()["ambulance_locations"]
        }

    @mcp.resource(
        "sentinel://hospital/bed-capacity",
        name="bed_capacity",
        mime_type="application/json",
    )
    def bed_capacity() -> dict:
        return {
            "bed_capacity":
            hospital_service.resources()["bed_capacity"]
        }

    @mcp.prompt(
        name="medical_emergency_sop",
        description="Standard Operating Procedure for medical emergency coordination."
    )
    def medical_emergency_sop(
        incident_type: str = "mass-casualty emergency"
    ) -> str:

        return (
            f"You are the SentinelOS Medical Emergency Coordinator.\n\n"
            f"Incident Type: {incident_type}\n\n"

            "Prepare a professional emergency coordination report including:\n\n"

            "1. Incident overview.\n"
            "2. Immediate life-saving priorities.\n"
            "3. Casualty triage strategy.\n"
            "4. Ambulance dispatch recommendations.\n"
            "5. Nearest suitable hospitals.\n"
            "6. ICU availability assessment.\n"
            "7. Bed availability summary.\n"
            "8. Medical team allocation.\n"
            "9. Required medical specializations.\n"
            "10. Resource shortages if any.\n"
            "11. Escalation procedure.\n"
            "12. Public medical advisory.\n"
            "13. Operational confidence level.\n\n"

            "Provide concise, structured emergency coordination guidance."
        )

    @mcp.prompt(
        name="triage_guidelines",
        description="Medical triage and casualty prioritization guidelines."
    )
    def triage_guidelines(
        context: str = "emergency incident"
    ) -> str:

        return (
            f"You are the SentinelOS Triage Coordinator.\n\n"
            f"Context: {context}\n\n"

            "Classify patients using standard emergency priorities:\n\n"

            "🔴 Immediate (Critical)\n"
            "- Life-threatening injuries\n"
            "- Immediate surgery or ICU required\n\n"

            "🟡 Delayed (Serious)\n"
            "- Serious but stable injuries\n"
            "- Requires hospital treatment soon\n\n"

            "🟢 Minor\n"
            "- Walking wounded\n"
            "- Basic treatment required\n\n"

            "⚫ Deceased / Expectant\n"
            "- No signs of life or survival unlikely\n\n"

            "Recommend:\n"
            "- Ambulance allocation\n"
            "- Hospital assignment\n"
            "- ICU prioritization\n"
            "- Bed allocation\n"
            "- Medical team deployment\n"
            "- Resource optimization\n"
            "- Escalation if hospitals become overloaded.\n\n"

            "This is operational guidance only and not a medical diagnosis."
        )