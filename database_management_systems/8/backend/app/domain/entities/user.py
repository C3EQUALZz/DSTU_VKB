from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Self, Any, Type

from app.domain.entities.base import BaseEntity
from app.domain.values.users import Email, Username, Password


@dataclass(eq=False)
class UserEntity(BaseEntity):
    name: Username
    email: Email
    password: Password

    is_active: bool = field(default=True, kw_only=True)
    is_superuser: bool = field(default=False, kw_only=True)
    is_verified: bool = field(default=False, kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_document(cls: Type[Self], document: Mapping[str, Any]) -> Self:
        oid = document["oid"]
        email = Email(value=document["email"])
        username = Username(value=document["name"])
        password = Password(value=document["password"])
        created_at = document["created_at"]
        is_verified = document["is_verified"]

        return cls(
            oid=oid,
            email=email,
            name=username,
            password=password,
            created_at=created_at,
            is_verified=is_verified
        )
