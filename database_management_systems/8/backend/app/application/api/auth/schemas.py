from typing import Optional, Self

from app.domain.entities.user import UserEntity
from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class UserSchemeResponse(BaseModel):
    name: str
    email: str
    oid: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(name=entity.name.as_generic_type(), email=entity.email.as_generic_type(), oid=entity.oid)
