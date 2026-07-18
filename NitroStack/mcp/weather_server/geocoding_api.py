from dotenv import load_dotenv
import os
import requests

# Load .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# OpenWeather Geocoding API
BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"


def geocode(city):
    params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            return {
                "success": False,
                "message": "City not found"
            }

        return {
            "success": True,
            "city": data[0]["name"],
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "country": data[0]["country"]
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": str(e)
        }