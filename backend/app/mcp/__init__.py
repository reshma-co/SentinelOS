from mcp.server.fastmcp import FastMCP

from .hospital import register_hospital_module
from .police import register_police_module
from .transport import register_transport_module
from .weather import register_weather_module


def register_all_modules(mcp: FastMCP) -> None:
    register_weather_module(mcp)
    register_hospital_module(mcp)
    register_police_module(mcp)
    register_transport_module(mcp)
