from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .services import TransportService

transport_service = TransportService()


def register_transport_module(mcp: FastMCP) -> None:

    @mcp.tool(
        description="Find available rescue or logistics vehicles near a location."
    )
    def find_rescue_vehicle(
        location: str,
        vehicle_type: str,
        radius_km: float = 15,
    ) -> dict:

        if not location.strip() or not vehicle_type.strip():
            raise ValueError("location and vehicle_type are required")

        return transport_service.find_rescue_vehicle(
            location.strip(),
            vehicle_type.strip(),
            radius_km,
        )

    @mcp.tool(
        description="Plan a vehicle route while accounting for blocked roads and vehicle restrictions."
    )
    def route_planning(
        origin: str,
        destination: str,
        vehicle_type: str,
        blocked_roads: list[str] | None = None,
    ) -> dict:

        if (
            not origin.strip()
            or not destination.strip()
            or not vehicle_type.strip()
        ):
            raise ValueError(
                "origin, destination, and vehicle_type are required"
            )

        return transport_service.route_planning(
            origin.strip(),
            destination.strip(),
            vehicle_type.strip(),
            blocked_roads,
        )

    @mcp.resource(
        "sentinel://transport/vehicles",
        name="vehicle_database",
        mime_type="application/json",
    )
    def vehicle_database() -> dict:
        return transport_service.vehicle_resource()

    @mcp.prompt(
        name="logistics_planning",
        description="Emergency rescue vehicle deployment and logistics planning."
    )
    def logistics_planning(
        location: str = "the incident area"
    ) -> str:

        return (
            f"You are the SentinelOS Transport & Logistics Coordination Module.\n\n"
            f"Incident Location: {location}\n\n"

            "Generate a professional emergency logistics report including:\n\n"

            "1. Incident overview.\n"
            "2. Required rescue vehicle types.\n"
            "3. Available rescue vehicles nearby.\n"
            "4. Vehicle allocation strategy.\n"
            "5. Rescue vehicle priorities.\n"
            "6. Best deployment routes.\n"
            "7. Alternate routes if roads are blocked.\n"
            "8. Flooded or inaccessible road analysis.\n"
            "9. Estimated travel time.\n"
            "10. Relief material transportation plan.\n"
            "11. Evacuation logistics.\n"
            "12. Fuel and resource requirements.\n"
            "13. Coordination with Police and Hospital modules.\n"
            "14. Logistics risk assessment (LOW, MODERATE, HIGH, CRITICAL).\n"
            "15. Operational confidence level.\n\n"

            "Present the response as a structured emergency logistics report with clear recommendations."
        )