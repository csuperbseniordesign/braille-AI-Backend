from pydantic import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Load the .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    SECRET_KEY: str
    PORT: int = 8000

    class Config:
        env_file = '.env'

# Create a single global instance
settings = Settings()