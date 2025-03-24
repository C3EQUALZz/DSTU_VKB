import uuid
from typing import Self
from typing import cast, Annotated, Literal

from pydantic import BaseModel, EmailStr, Field, AfterValidator, UUID4

from app.domain.entities.user import UserEntity


class UserSchemaResponse(BaseModel):
    oid: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    name: str = Field(min_length=1, max_length=40)
    surname: str = Field(min_length=1, max_length=40)
    patronymic: str = Field(min_length=1, max_length=40)
    email: EmailStr
    role: Literal["staffer", "admin", "manager"]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(
            surname=entity.surname,
            patronymic=entity.patronymic,
            name=entity.name,
            email=cast(EmailStr, entity.email.as_generic_type()),
            oid=entity.oid,
            role=cast(Literal["staffer", "admin", "manager"], entity.role.as_generic_type()),
        )


class CreateUserSchemaRequest(BaseModel):
    surname: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=40)
    patronymic: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UpdateUserSchemaRequest(BaseModel):
    oid: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    surname: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=40)
    patronymic: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
