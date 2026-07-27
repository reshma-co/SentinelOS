from __future__ import annotations

import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl


EXPECTED_TOOLS = {
    "weather_forecast": {"location": "Chennai"},
    "flood_prediction": {"location": "Chennai", "rainfall_mm": 95, "drainage_capacity": "poor"},
    "find_hospital": {"location": "Chennai", "emergency_type": "trauma", "radius_km": 10},
    "check_icu": {"hospital_id_or_name": "HSP-CHN-001"},
    "find_ambulance": {"location": "Velachery", "radius_km": 10},
    "allocate_medical_team": {"incident_location": "Velachery", "emergency_severity": "critical", "required_specialization": "trauma"},
    "find_safe_route": {"origin": "Chennai Central", "destination": "Tambaram", "blocked_roads": ["Velachery Main Road"]},
    "report_road_block": {"road_location": "OMR", "reason": "waterlogging", "severity": "moderate"},
    "assign_officers": {"incident_location": "Velachery", "required_number_of_officers": 4, "priority": "high"},
    "find_rescue_vehicle": {"location": "Velachery", "vehicle_type": "rescue boat", "radius_km": 15},
    "route_planning": {"origin": "Chennai Central", "destination": "Velachery", "vehicle_type": "bus", "blocked_roads": ["Velachery Main Road"]},
}

EXPECTED_RESOURCES = {
    "weather_api": "sentinel://weather/api",
    "hospital_database": "sentinel://hospital/database",
    "ambulance_locations": "sentinel://hospital/ambulances",
    "bed_capacity": "sentinel://hospital/bed-capacity",
    "road_database": "sentinel://police/roads",
    "traffic_reports": "sentinel://police/traffic-reports",
    "vehicle_database": "sentinel://transport/vehicles",
}

EXPECTED_PROMPTS = {
    "weather_risk_analysis": {"location": "Chennai"},
    "medical_emergency_sop": {"incident_type": "flood emergency"},
    "triage_guidelines": {"context": "flood evacuation"},
    "evacuation_protocol": {"location": "Velachery"},
    "logistics_planning": {"location": "Velachery"},
}


async def main() -> None:
    server_path = Path(__file__).with_name("server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server_path)])

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = {tool.name for tool in tools.tools}
            missing_tools = sorted(set(EXPECTED_TOOLS) - tool_names)
            if missing_tools:
                raise SystemExit(f"Missing tools: {missing_tools}")

            for name, args in EXPECTED_TOOLS.items():
                result = await session.call_tool(name, args)
                if result.isError:
                    raise SystemExit(f"Tool failed: {name}")
                print(f"[tool] {name}: ok")

            resources = await session.list_resources()
            resource_names = {resource.name for resource in resources.resources}
            missing_resources = sorted(set(EXPECTED_RESOURCES) - resource_names)
            if missing_resources:
                raise SystemExit(f"Missing resources: {missing_resources}")

            for name, uri in EXPECTED_RESOURCES.items():
                result = await session.read_resource(AnyUrl(uri))
                if not result.contents:
                    raise SystemExit(f"Resource empty: {name}")
                print(f"[resource] {name}: ok")

            prompts = await session.list_prompts()
            prompt_names = {prompt.name for prompt in prompts.prompts}
            missing_prompts = sorted(set(EXPECTED_PROMPTS) - prompt_names)
            if missing_prompts:
                raise SystemExit(f"Missing prompts: {missing_prompts}")

            for name, args in EXPECTED_PROMPTS.items():
                result = await session.get_prompt(name, args)
                if not result.messages:
                    raise SystemExit(f"Prompt empty: {name}")
                print(f"[prompt] {name}: ok")

            print("All SentinelOS modules verified.")


if __name__ == "__main__":
    asyncio.run(main())
