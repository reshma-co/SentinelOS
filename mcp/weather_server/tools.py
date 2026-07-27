from weather_api import get_weather


def weather_tool(city: str):
    """
    Returns live weather data for the given city.
    """
    return get_weather(city)