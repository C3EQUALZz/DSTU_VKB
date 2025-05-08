from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserRegisterEventForBrokerSchema(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Users name for publishing in another microservices"
    )

    surname: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Users surname for publishing in another microservices"
    )

    role: Literal["user", "admin"] = Field(
        default="user",
        validate_default=True,
        description="user role"
    )


class UserSendEmailForVerificationSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email address"
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Users name for publishing in another microservices"
    )

    surname: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Users surname for publishing in another microservices"
    )
