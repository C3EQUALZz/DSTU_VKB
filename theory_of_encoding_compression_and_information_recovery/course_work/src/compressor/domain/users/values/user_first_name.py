from dataclasses import dataclass

from typing_extensions import override

from compressor.domain.common.values.base import BaseValueObject
from compressor.domain.users.errors import EmptyFieldError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class UserFirstName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value.isspace() or self.value == '':
            raise EmptyFieldError("Telegram name cannot be empty string, please provide a info")

    def __len__(self) -> int:
        return len(self.value)

    @override
    def __str__(self) -> str:
        return self.value
