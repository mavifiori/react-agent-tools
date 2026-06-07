import requests
from langchain_core.tools import tool

from src.config import OPENWEATHER_API_KEY
from src.tools._geocoding import geocode_city

_UV_API_URL = "https://api.open-meteo.com/v1/forecast"

_UV_INDEX_LABELS = [
    (0, 2.99, "Low - no protection required"),
    (3, 5.99, "Moderate - use sunscreen and wear sunglasses on bright days"),
    (6, 7.99, "High - protection required"),
    (8, 10.99, "Very High - protection essential"),
    (11, float("inf"), "Extreme - seek shade and use protection"),
]

    
def _classify_uv_index(uv_index: float) -> str:
    for low, high, label in _UV_INDEX_LABELS:
        if low <= uv_index <= high:
            return label
    return "Extreme"


@tool
def get_uv_index(city: str) -> str:
    """Returns the current UV index for a city. 
    Use when the user asks about the UV index or sun exposure in a location."""
   
    location = geocode_city(city)
    if isinstance(location, str):
        return location  
    lat, lon = location
    
    try:
        uv_response = requests.get(
            _UV_API_URL,
            params={"latitude": lat, "longitude": lon,"current":"uv_index"},
            timeout=5,
        )
        uv_response.raise_for_status()
        uv_value =float| uv_response.json().get("current", {}).get("uv_index")
        if uv_value is None:
            return f"UV index data not available for {city}."
        return f"The current UV index in {city} is {uv_value:.1f} - {_classify_uv_index(uv_value)}."
    except requests.exceptions.Timeout:
        return f"Error: request Timeout"
    except requests.exceptions.RequestException as e:
        return f"Error fetching UV index data: {e}"