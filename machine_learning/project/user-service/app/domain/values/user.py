from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import WrongUserRole


@dataclass
class Role(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("bot", "user", "admin"):
            raise WrongUserRole(f"Bad role of user: {self.value}")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
