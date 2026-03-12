from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from pydantic import model_validator
from typing import Literal, Self

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn | None = None
    API_VERSION: str = "1.0"
    ENVIRONMENT: Literal["LOCAL", "PRODUCTION"]
    DATABASE_PARAMETER_NAME: str | None = None
    API_PORT: int = Field(ge=1024, le=49151)

    @model_validator(mode="after")
    def validate_database_url(self) -> Self:
        if self.ENVIRONMENT == "LOCAL" and not self.DATABASE_URL:
            raise ValueError("'DATABASE_URL' not set in local environment")
        if self.ENVIRONMENT == "PRODUCTION" and not self.DATABASE_PARAMETER_NAME:
            raise ValueError("'DATABASE_PARAMETER_NAME' not set in production environment")
        return self