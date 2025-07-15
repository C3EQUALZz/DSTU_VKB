from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject
from cryptography_methods.domain.user.errors import (
    UserNameCantBeEmptyStringError,
    UserNameCantBeNumberError,
    UserNameLengthError
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class FirstName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, str):
            raise TypeError("Имя пользователя должно быть строкой")

        if self.value.isspace():
            raise UserNameCantBeEmptyStringError("Имя пользователя не может быть пустой строкой")

        if self.value.isnumeric():
            raise UserNameCantBeNumberError("Имя пользователя не может быть цифрами")

        if not 1 <= len(self.value) <= 255:
            raise UserNameLengthError("Длина пользовательского имени должна находится в диапазоне от 1 до 255")

    @override
    def __str__(self) -> str:
        return str(self.value)
