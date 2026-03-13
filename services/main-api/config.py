from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    Field,
    model_validator, 
    computed_field
)
from typing import Literal, Self
import os

from constants import SECRETS_DIR

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        secrets_dir=SECRETS_DIR if os.path.isdir(SECRETS_DIR) else None,
        extra="allow"
    )

    API_VERSION: str = "1.0"
    ENVIRONMENT: Literal["LOCAL", "DOCKER", "PRODUCTION"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    API_PORT: int = Field(ge=1024, le=49151)

    DATABASE_URL: PostgresDsn | None = None
    DATABASE_PARAMETER_NAME: str | None = None
    db_password: str | None = None

    @model_validator(mode="after")
    def validate_database_url(self) -> Self:
        if self.ENVIRONMENT == "LOCAL" and not self.DATABASE_URL:
            raise ValueError("'DATABASE_URL' not set in local environment")
        if self.ENVIRONMENT == "DOCKER":
            if not self.db_password:
                raise ValueError("'db_password' secret not found")
            self.DATABASE_URL = f"postgresql://postgres:{self.db_password}@database:5432/research-assistant"
        if self.ENVIRONMENT == "PRODUCTION" and not self.DATABASE_PARAMETER_NAME:
            raise ValueError("'DATABASE_PARAMETER_NAME' not set in production environment")
        return self
    
    @computed_field
    @property
    def LOG_LEVEL_PARSED(self) -> int:
        level_mappings = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }
        return level_mappings.get(self.LOG_LEVEL, 20)
    
settings = Config()