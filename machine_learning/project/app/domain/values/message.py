from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyTextException


@dataclass
class Text(BaseValueObject[str]):
    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException("Message can't be empty, please write some info")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
