import requests
from langchain_core.tools import tool

from src.config import OPENWEATHER_API_KEY
from src.tools._geocoding import geocode_city

_AIR_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

_AIR_QUALITY_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor"
}

    
def _classify_air_quality(aqi: int) -> str:
    for key, label in _AIR_QUALITY_LABELS.items():
        if isinstance(key, tuple):
            low, high = key
            if low <= aqi <= high:
                return label
        elif aqi == key:
            return label
    return "Very Poor"


@tool
def get_air_quality(city: str) -> str:
    """Returns the current air quality for a city.
    Use when the user asks about air quality in a location."""
    try:
    
        location = geocode_city(city)
        if isinstance(location, str):
            return location  
        lat, lon = location

        air_response = requests.get(
            _AIR_API_URL,
            params={"lat": lat, "lon": lon,"appid": OPENWEATHER_API_KEY},
            timeout=5,
        )
        
        if air_response.status_code == 401:
                return f"Invalid API key for weather service."
        air_response.raise_for_status()
        
        aqi: int | None = air_response.json().get("list", [{}])[0].get("main", {}).get("aqi")
        if aqi is None:
            return f"Air quality data not available for {city}."
        
        return f"The current air quality in {city} is {aqi} ({_classify_air_quality(aqi)})."
    
    except requests.exceptions.Timeout:
        return f"Error: request Timeout"
    except requests.exceptions.RequestException as e:
        return f"Error fetching air quality data: {e}"