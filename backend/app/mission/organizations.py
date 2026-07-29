from __future__ import annotations

import asyncio
from typing import Any

from app.mcp.services import (
    WeatherService,
    HospitalService,
    PoliceService,
    TransportService,
)
from .capability_registry import CAPABILITY_TO_MODULE
from .schemas import MissionContext, OrgResponse

# Instantiate service singletons
weather_svc = WeatherService()
hospital_svc = HospitalService()
police_svc = PoliceService()
transport_svc = TransportService()


def _capabilities_for_org(org: str, required_capabilities: list[str]) -> list[str]:
    return [
        cap for cap in required_capabilities if org in CAPABILITY_TO_MODULE.get(cap, [])
    ]


async def weather_handler(context: MissionContext) -> OrgResponse:
    service = WeatherService()
    # Pass incident_type / description so services.py uses scenario logic
    res = service.flood_prediction(
        location=context.location, incident_description=context.incident_type
    )

    # Build dynamic summary and recommendations based on incident type
    inc_type = context.incident_type.lower()
    if "earthquake" in inc_type or "seismic" in inc_type:
        summary = f"Seismic hazard evaluated as {res.get('seismic_hazard_level', 'HIGH')} for {context.location}."
    elif "chemical" in inc_type or "leak" in inc_type:
        summary = f"Hazmat risk evaluated as {res.get('hazmat_hazard_level', 'CRITICAL')} for {context.location}."
    elif "power" in inc_type or "outage" in inc_type:
        summary = f"Grid hazard evaluated as {res.get('grid_hazard_level', 'HIGH')} for {context.location}."
    else:
        summary = f"Flood risk assessed as {res.get('flood_risk_level', 'HIGH')} for {context.location}."

    return OrgResponse(
        organization="weather",
        status="ok",
        capabilities_covered=context.required_capabilities,
        summary=summary,
        recommendations=res.get("recommended_precautions", []),
        resources=[
            f"Rainfall score: {res.get('rainfall_information', {}).get('score', 0)}"
        ],
        raw=res,
    )


async def hospital(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("hospital", context.required_capabilities)

    # Query real dataset service
    hospitals_data = hospital_svc.find_hospital(location=context.location, radius_km=15)
    ambulances_data = hospital_svc.find_ambulance(
        location=context.location, radius_km=15
    )

    count = hospitals_data.get("count", 0)
    matched = hospitals_data.get("matching_hospitals", [])
    rec_list = [
        f"Direct patients to {h['name']} ({h['location']})" for h in matched
    ] or ["No nearby hospital found in database"]

    return OrgResponse(
        organization="hospital",
        status="ok",
        capabilities_covered=caps,
        summary=f"Found {count} matching hospital(s) and {ambulances_data.get('count', 0)} available ambulance(s) near {context.location}.",
        recommendations=rec_list,
        resources=[
            f"{len(ambulances_data.get('available_ambulances', []))} ambulances ready"
        ],
        raw={"hospitals": hospitals_data, "ambulances": ambulances_data},
    )


async def police(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("police", context.required_capabilities)

    # Query real route planning
    route_data = police_svc.find_safe_route(
        origin=context.location, destination="Safe Zone Shelter"
    )

    return OrgResponse(
        organization="police",
        status="ok",
        capabilities_covered=caps,
        summary=f"Safe route calculated avoiding blocked roads: {', '.join(route_data['blocked_roads_avoided']) or 'none'}.",
        recommendations=[
            f"Evacuate via route: {' -> '.join(route_data['recommended_safe_route'])}"
        ],
        resources=["Police traffic units dispatched"],
        raw=route_data,
    )


async def transport_handler(context: MissionContext) -> OrgResponse:
    service = TransportService()
    res = service.find_rescue_vehicle(
        location=context.location, incident_description=context.incident_type
    )

    inc_type = context.incident_type.lower()
    if "earthquake" in inc_type:
        recs = ["Deploy heavy debris clearance trucks and structural rescue vehicles."]
    elif "chemical" in inc_type:
        recs = ["Deploy evacuation buses outside the exclusion zone."]
    else:
        recs = ["Deploy rescue boats to flooded wards."]

    vehicles = res.get("available_rescue_vehicles", [])
    vehicle_summary = (
        f"{vehicles[0]['type']} at {vehicles[0]['location']}"
        if vehicles
        else "No vehicles matched"
    )

    return OrgResponse(
        organization="transport",
        status="ok",
        capabilities_covered=context.required_capabilities,
        summary=f"Transport assessment complete. Found {res.get('count', 0)} rescue vehicle(s).",
        recommendations=recs,
        resources=[vehicle_summary],
        raw=res,
    )


async def volunteer(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("volunteer", context.required_capabilities)
    return OrgResponse(
        organization="volunteer",
        status="ok",
        capabilities_covered=caps,
        summary="Volunteer mobilization active.",
        recommendations=["Open local community shelter", "Distribute intake packages"],
        resources=["20 field volunteers"],
        raw={},
    )


async def communication(context: MissionContext) -> OrgResponse:
    await asyncio.sleep(0.05)
    caps = _capabilities_for_org("communication", context.required_capabilities)
    return OrgResponse(
        organization="communication",
        status="ok",
        capabilities_covered=caps,
        summary=f"Public safety alert generated for {context.location}.",
        recommendations=[
            "Broadcast weather and route advisories over SMS/Emergency radio"
        ],
        resources=["Emergency Alert System"],
        raw={},
    )


ORGANIZATION_HANDLERS = {
    "weather": weather_handler,
    "hospital": hospital,
    "police": police,
    "transport": transport_handler,
    "volunteer": volunteer,
    "communication": communication,
}
