from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class RegisterUserSchemaRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40, description="User name for application")
    surname: str = Field(min_length=2, max_length=40, description="User surname for application")
    password: str = Field(min_length=1, max_length=255, description="Password for user")
    email: EmailStr = Field(..., description="Email address for user")

