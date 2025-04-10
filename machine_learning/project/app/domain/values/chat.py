from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import (BadChatTypeError, EmptyTextError,
                                   TitleTooLongError)


@dataclass
class Title(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextError("Text cannot be empty")

        if len(self.value) > 255:
            raise TitleTooLongError("Please provide more short title ")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ChatType(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextError("Chat type cannot be empty")

        if self.value not in ("private", "group", "supergroup"):
            raise BadChatTypeError("Chat type must be 'private' or 'group' or 'supergroup'")

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
