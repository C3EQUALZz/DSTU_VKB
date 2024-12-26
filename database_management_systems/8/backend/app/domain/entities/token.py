from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Self

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class Token(BaseEntity, ABC):
    sub: str
    exp: datetime
    iat: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)

    __eq__ = BaseEntity.__eq__
    __hash__ = BaseEntity.__hash__

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Self:
        ...


@dataclass(eq=False)
class AccessToken(Token):
    @classmethod
    def from_dict(cls, payload: dict) -> "AccessToken":
        """Создает AccessToken из словаря."""
        return cls(
            sub=payload["sub"],
            exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
            iat=datetime.fromtimestamp(payload.get("iat", datetime.now(UTC).timestamp()), tz=UTC),
        )


@dataclass(eq=False)
class RefreshToken(Token):
    refresh_token: str

    @classmethod
    def from_dict(cls, payload: dict) -> "RefreshToken":
        return cls(
            sub=payload["sub"],
            exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
            iat=datetime.fromtimestamp(payload.get("iat", datetime.now(UTC).timestamp()), tz=UTC),
            refresh_token=payload["refresh_token"],
        )
