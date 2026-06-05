import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.environ["GROQ_API_KEY"]
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")
OPENWEATHER_API_KEY: str = os.environ["OPENWEATHER_API_KEY"]