from typing import Self

from app.domain.entities.user import UserEntity
from pydantic import BaseModel


class CreateUserSchemaRequest(BaseModel):
    name: str
    email: str
    password: str


class UpdateUserSchemaRequest(BaseModel):
    name: str
    email: str
    password: str


class ErrorMessageScheme(BaseModel):
    error: str


class UserSchemeResponse(BaseModel):
    name: str
    email: str
    oid: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(name=entity.name, email=entity.email, oid=entity.oid)
