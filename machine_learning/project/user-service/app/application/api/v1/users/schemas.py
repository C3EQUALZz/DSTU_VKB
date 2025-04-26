from typing import Literal, Self, cast

from pydantic import BaseModel, Field

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
            first_name=entity.first_name,
            role=cast(Literal["bot", "user", "admin"], entity.role.as_generic_type()),
        )


class CreateUserSchemaRequest(BaseModel):
    first_name: str = Field(min_length=2, max_length=40)


class UpdateUserSchemaRequest(CreateUserSchemaRequest):
    oid: StringUUID
