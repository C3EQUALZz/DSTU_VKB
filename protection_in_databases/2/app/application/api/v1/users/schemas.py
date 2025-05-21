from typing import Annotated, Self
from typing import Literal, cast
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, Field, PlainSerializer
from pydantic import EmailStr

from app.domain.entities.user import UserEntity

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]


class UserSchemaResponse(BaseModel):
    oid: StringUUID
    name: str = Field(min_length=1, max_length=40)
    surname: str = Field(min_length=1, max_length=40)
    role: Literal["bot", "user", "admin"]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(
            oid=UUID(entity.oid),
            name=entity.name,
            surname=entity.surname,
            role=cast(Literal["bot", "user", "admin"], entity.role.as_generic_type()),
        )


class CreateUserSchemaRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40, description="User name for application")
    surname: str = Field(min_length=2, max_length=40, description="User surname for application")
    password: str = Field(min_length=1, max_length=255, description="Password for user")
    email: EmailStr = Field(..., description="Email address for user")


class UpdateUserSchemaRequest(CreateUserSchemaRequest):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="User name for updating, this field is Optional"
    )

    surname: str | None = Field(
        default=None,
        min_length=1,
        max_length=40,
        description="User surname for updating, this field is Optional"
    )

    email: EmailStr | None = Field(
        default=None,
        description="Email address for user"
    )

    role: Literal["bot", "user", "admin"] | None = Field(
        default="user",
        validate_default=True
    )
