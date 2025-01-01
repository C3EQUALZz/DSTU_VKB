from dataclasses import dataclass
from typing import override
from uuid import UUID

from app.domain.exceptions import (
    EmptyScoreException,
    InvalidOIDException,
)
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class UserOID(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        try:
            uuid_obj = UUID(self.value)
            assert str(uuid_obj) == self.value
        except (ValueError, AssertionError):
            raise InvalidOIDException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ScoreValue(BaseValueObject[int]):
    value: int

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyScoreException(str(self.value))

    @override
    def as_generic_type(self) -> int:
        return int(self.value)
