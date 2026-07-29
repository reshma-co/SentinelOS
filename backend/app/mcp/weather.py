from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .services import WeatherService

weather_service = WeatherService()


def register_weather_module(mcp: FastMCP) -> None:

    @mcp.tool(
        description="Return current weather and short forecast intelligence for an emergency location."
    )
    def weather_forecast(
        location: str,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict:
        if not location.strip():
            raise ValueError("location is required")

        return weather_service.forecast(
            location.strip(),
            latitude,
            longitude,
        )

    @mcp.tool(
        description="Estimate flood risk from rainfall, drainage, river level, and soil saturation signals."
    )
    def flood_prediction(
        location: str,
        rainfall_mm: float | None = None,
        forecast_rainfall_mm: float | None = None,
        drainage_capacity: str = "moderate",
        river_level: str = "normal",
        soil_saturation: str = "moderate",
    ) -> dict:

        if not location.strip():
            raise ValueError("location is required")

        return weather_service.flood_prediction(
            location.strip(),
            rainfall_mm,
            forecast_rainfall_mm,
            drainage_capacity,
            river_level,
            soil_saturation,
        )

    @mcp.resource(
        "sentinel://weather/api",
        name="weather_api",
        description="Structured weather and environmental records used by WeatherModule.",
        mime_type="application/json",
    )
    def weather_api() -> dict:
        return weather_service.weather_resource()

    @mcp.prompt(
        name="weather_risk_analysis",
        description="Analyze weather conditions, rainfall, flood severity, high-risk areas, and emergency actions.",
    )
    def weather_risk_analysis(location: str = "the incident area") -> str:

        return (
            f"You are the SentinelOS Weather Intelligence Module.\n\n"
            f"Analyze the weather conditions for {location}.\n\n"

            "Generate a professional disaster weather assessment including:\n\n"

            "1. Current weather summary.\n"
            "2. Temperature, humidity and wind conditions.\n"
            "3. Current rainfall and forecast rainfall.\n"
            "4. Flood probability assessment.\n"
            "5. Flood severity (LOW, MODERATE, HIGH or CRITICAL).\n"
            "6. Identify high-risk or low-lying areas.\n"
            "7. Mention possible impacts on roads, hospitals and public transport.\n"
            "8. Recommend evacuation if necessary.\n"
            "9. Recommend emergency response actions.\n"
            "10. Suggest deployment of rescue teams and relief resources.\n"
            "11. Suggest public safety advisories.\n"
            "12. Mention confidence level and any uncertainty in the prediction.\n\n"

            "Present the output in a clear, structured emergency report."
        )