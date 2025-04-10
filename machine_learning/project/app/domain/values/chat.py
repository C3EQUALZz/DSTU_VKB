from dataclasses import dataclass
from typing import override
from app.domain.values.base import BaseValueObject
from app.exceptions.domain import EmptyTextException, TitleTooLongException


@dataclass
class Title(BaseValueObject[str]):
    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException("Text cannot be empty")

        if len(self.value) > 255:
            raise TitleTooLongException("Please provide more short title ")

    def as_generic_type(self) -> str:
        return str(self.value)