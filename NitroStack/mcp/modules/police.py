from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .services import PoliceService

police_service = PoliceService()


def register_police_module(mcp: FastMCP) -> None:

    @mcp.tool(
        description="Recommend a safe evacuation or response route while avoiding blocked roads."
    )
    def find_safe_route(
        origin: str,
        destination: str,
        blocked_roads: list[str] | None = None,
    ) -> dict:

        if not origin.strip() or not destination.strip():
            raise ValueError("origin and destination are required")

        return police_service.find_safe_route(
            origin.strip(),
            destination.strip(),
            blocked_roads,
        )

    @mcp.tool(
        description="Report a road block or unsafe road condition."
    )
    def report_road_block(
        road_location: str,
        reason: str,
        severity: str,
        description: str | None = None,
    ) -> dict:

        if not road_location.strip() or not reason.strip():
            raise ValueError("road_location and reason are required")

        return police_service.report_road_block(
            road_location.strip(),
            reason.strip(),
            severity,
            description,
        )

    @mcp.tool(
        description="Assign police officers or a police unit to an incident location."
    )
    def assign_officers(
        incident_location: str,
        required_number_of_officers: int,
        priority: str,
    ) -> dict:

        if required_number_of_officers <= 0:
            raise ValueError("required_number_of_officers must be positive")

        return police_service.assign_officers(
            incident_location.strip(),
            required_number_of_officers,
            priority,
        )

    @mcp.resource(
        "sentinel://police/roads",
        name="road_database",
        mime_type="application/json",
    )
    def road_database() -> dict:
        return {
            "road_database":
            police_service.resources()["road_database"]
        }

    @mcp.resource(
        "sentinel://police/traffic-reports",
        name="traffic_reports",
        mime_type="application/json",
    )
    def traffic_reports() -> dict:
        return {
            "traffic_reports":
            police_service.resources()["traffic_reports"]
        }

    @mcp.prompt(
        name="evacuation_protocol",
        description="Emergency evacuation planning and police coordination."
    )
    def evacuation_protocol(
        location: str = "the incident zone"
    ) -> str:

        return (
            f"You are the SentinelOS Police Coordination Module.\n\n"
            f"Incident Location: {location}\n\n"

            "Generate a complete evacuation and law enforcement coordination report including:\n\n"

            "1. Incident overview.\n"
            "2. Road closure assessment.\n"
            "3. Traffic congestion analysis.\n"
            "4. Flooded or unsafe road identification.\n"
            "5. Recommended safe evacuation routes.\n"
            "6. Alternate evacuation routes.\n"
            "7. Police officer deployment plan.\n"
            "8. Crowd management recommendations.\n"
            "9. Security for hospitals and shelters.\n"
            "10. Emergency vehicle access routes.\n"
            "11. Public traffic advisory.\n"
            "12. Coordination with transport and medical teams.\n"
            "13. Incident priority (LOW, MODERATE, HIGH, CRITICAL).\n"
            "14. Operational confidence level.\n\n"

            "Present the response as a structured emergency operations report."
        )