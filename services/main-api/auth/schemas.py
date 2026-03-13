from pydantic import (
    BaseModel, 
    Field,
    EmailStr,
    SecretStr,
    field_validator
)
import re

class UserSignUpBase(BaseModel):
    user_name: str = Field(max_length=25)
    email: EmailStr

class UserSignUpIn(UserSignUpBase):
    password: SecretStr = Field(
        min_length=12,
        description="Password must be at least 12 characters long."
    )

    # Had to use a field validator since PyDantic does not support lookaheads patterns
    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        #value = v.get_secret_value()

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[$&#!?%@.]", v):
            raise ValueError("Password must contain at least one symbol ($ & # ! ? % @ .).")
        return v

class UserSignUpOut(UserSignUpBase):
    ...