from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    database_url: str = "sqlite:///./iga.db"
    slack_bot_token: str = ""
    slack_signing_secret: str = ""
    secret_key: str = ""
    debug: bool = False

settings = Settings()