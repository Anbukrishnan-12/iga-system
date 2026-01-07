from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    # Use persistent database path for production
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/iga.db")
    slack_bot_token: str = ""
    slack_signing_secret: str = ""
    secret_key: str = ""
    debug: bool = False

settings = Settings()