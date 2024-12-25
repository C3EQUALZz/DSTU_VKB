from typing import Self

from app.domain.entities.user import UserEntity
from pydantic import BaseModel, EmailStr


class CreateUserSchemaRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UpdateUserSchemaRequest(BaseModel):
    oid: str
    name: str
    email: EmailStr
    password: str


class ErrorMessageScheme(BaseModel):
    error: str


class UserSchemeResponse(BaseModel):
    name: str
    email: str
    oid: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(name=entity.name.as_generic_type(), email=entity.email.as_generic_type(), oid=entity.oid)
