from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyTextError


@dataclass
class Text(BaseValueObject[str]):
    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextError("Message can't be empty, please write some info")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
