from langchain_core.tools import tool
import requests
from src.config import OPENWEATHER_API_KEY



_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@tool
def get_weather(city: str) -> str:
    """
    Returns the current weather conditions for a city. 
    Use when the user asks about the weather or temperature somewhere."""
    try:
        response = requests.get(
            _BASE_URL,
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "en",
            },
            timeout=5,
        )
        if response.status_code == 404:
            return f"City not found: {city}."
        if response.status_code == 401:
            return f"Invalid API key for weather service."

        response.raise_for_status()
        data: dict = response.json()
        
        return "\n".join([
            f"Current weather in {city}, {data['sys']['country']}: {data['weather'][0]['description']}",
                f"Temperature: {data['main']['temp']}°C (Feels like: {data['main']['feels_like']}°C)",
                f"Humidity: {data['main']['humidity']}%",
                f"Wind: {data['wind']['speed']} m/s"
        ])
    except requests.exceptions.Timeout:
        return f"Error fetching weather data: Timeout"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"