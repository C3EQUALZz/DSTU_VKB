from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject
from cryptography_methods.domain.user.errors import (
    UserMiddleNameCantBeEmptyString,
    UserMiddleNameCantBeNumberError,
    UserMiddleNameLengthError
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class MiddleName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, str):
            raise TypeError("Отчество должно быть строкой")

        if self.value.isspace():
            raise UserMiddleNameCantBeEmptyString("Отчество не может быть пустой строкой")

        if self.value.isnumeric():
            raise UserMiddleNameCantBeNumberError("Отчество не может быть цифрой")

        if not 1 <= len(self.value) <= 255:
            raise UserMiddleNameLengthError("Отчество может быть только в диапазоне от 1 до 255")

    @override
    def __str__(self) -> str:
        return str(self.value)
