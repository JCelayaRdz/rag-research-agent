from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from datetime import timedelta
from typing_extensions import Self
import os

from ..config import settings
from ..constants import SECRETS_DIR

class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../env",
        secrets_dir=SECRETS_DIR if os.path.isdir(SECRETS_DIR) else None,
        extra="allow"
    )

    JWT_ALG: str
    JWT_SECRET: str | None = None
    JWT_SECRET_PARAMETER_NAME: str | None = None
    JWT_EXP: int = 25
    REFRESH_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET_PARAMETER_NAME: str | None = None
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=7)

    @model_validator(mode="after")
    def validate_token_secret(self) -> Self:
        if settings.ENVIRONMENT == "LOCAL" or settings.ENVIRONMENT == "DOCKER":
            if not self.JWT_SECRET:
                raise ValueError(f"'JWT_SECRET' not set in {settings.ENVIRONMENT.lower()} environment")
            if not self.REFRESH_TOKEN_SECRET:
                raise ValueError(f"'REFRESH_TOKEN_SECRET' not set in {settings.ENVIRONMENT.lower()} environment")
                            
        if settings.ENVIRONMENT == "PRODUCTION":
            if not self.JWT_SECRET_PARAMETER_NAME:
                raise ValueError(f"'JWT_SECRET_PARAMETER_NAME' not set in production environment")
            if not self.REFRESH_TOKEN_SECRET_PARAMETER_NAME:
                raise ValueError(f"'REFRESH_TOKEN_SECRET_PARAMETER_NAME' not set in production environment")
        return self
    
settings = AuthConfig()