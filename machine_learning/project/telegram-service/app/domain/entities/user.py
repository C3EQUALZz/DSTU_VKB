from dataclasses import (
    dataclass,
)

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    oid: int
    full_name: str
    user_login: str
    role: str
    language_code: str
