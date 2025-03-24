from app.domain.values.base import BaseValueObject
from dataclasses import dataclass
from typing import override

from app.exceptions.domain import UnExistingPlatform


@dataclass
class Platform(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("twitter", "vk", "telegram"):
            raise UnExistingPlatform(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
