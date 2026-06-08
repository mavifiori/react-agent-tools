import requests
from src.config import OPENWEATHER_API_KEY
from typing import Union, Tuple

_GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"

def geocode_city(city: str) -> Union[Tuple[float, float], str]:
    """Returns the latitude and longitude(lat,lon) of a city."""
    try:
        response = requests.get(
            _GEO_URL,
            params={"q": city, "limit": 1, "appid": OPENWEATHER_API_KEY},
            timeout=5,
        )
        if response.status_code == 401:
            return f"Invalid API key for weather service."
        
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return f"City not found: {city}"
        
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon
    
    except requests.exceptions.Timeout:
        return "Error: geocoding request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error geocoding city: {e}"
    