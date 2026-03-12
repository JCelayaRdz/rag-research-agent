from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from pydantic import model_validator, computed_field
from typing import Literal, Self
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn | None = None
    API_VERSION: str = "1.0"
    ENVIRONMENT: Literal["LOCAL", "PRODUCTION"]
    DATABASE_PARAMETER_NAME: str | None = None
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    API_PORT: int = Field(ge=1024, le=49151)

    @model_validator(mode="after")
    def validate_database_url(self) -> Self:
        if self.ENVIRONMENT == "LOCAL" and not self.DATABASE_URL:
            raise ValueError("'DATABASE_URL' not set in local environment")
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