import uuid
from typing import Annotated, Literal, Self, cast

from pydantic import UUID4, AfterValidator, BaseModel, EmailStr, Field

from app.domain.entities.user import UserEntity


class UserSchemaResponse(BaseModel):
    id: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    name: str = Field(min_length=1, max_length=40)
    surname: str = Field(min_length=1, max_length=40)
    email: EmailStr
    role: Literal["user", "admin"]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(
            surname=entity.surname.as_generic_type(),
            name=entity.name.as_generic_type(),
            email=cast(EmailStr, entity.email.as_generic_type()),
            id=entity.id,
            role=cast(Literal["user", "admin"], entity.role.as_generic_type()),
        )


class CreateUserSchemaRequest(BaseModel):
    surname: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UpdateUserSchemaRequest(BaseModel):
    id: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    surname: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=40)
    role: Literal["user", "admin"] = Field(default="user")
