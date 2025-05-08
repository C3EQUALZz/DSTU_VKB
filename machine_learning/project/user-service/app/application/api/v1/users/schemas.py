from typing import Literal, Self, cast

from pydantic import BaseModel, Field, EmailStr

from app.application.api.v1.utils.schemas import StringUUID
from app.domain.entities.user import UserEntity


class UserSchemaResponse(BaseModel):
    oid: StringUUID
    first_name: str = Field(min_length=1, max_length=40)
    role: Literal["bot", "user", "admin"]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(
            oid=entity.oid,
            first_name=entity.name,
            role=cast(Literal["bot", "user", "admin"], entity.role.as_generic_type()),
        )


class CreateUserSchemaRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40, description="User name for application")
    surname: str = Field(min_length=2, max_length=40, description="User surname for application")
    password: str = Field(min_length=1, max_length=255, description="Password for user")
    email: EmailStr = Field(..., description="Email address for user")


class UpdateUserSchemaRequest(CreateUserSchemaRequest):
    id: StringUUID = Field(
        ...,
        description="Unique identifier of the user"
    )

    name: str = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="User name for updating, this field is Optional"
    )

    surname: str = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="User surname for updating, this field is Optional"
    )

    email: EmailStr = Field(
        default=None,
        description="Email address for user"
    )

    role: Literal["bot", "user", "admin"] = Field(
        default="user",
        validate_default=True
    )
