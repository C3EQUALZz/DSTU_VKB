from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject
from cryptography_methods.domain.user.errors import (
    UserSecondNameCantBeEmptyString,
    UserSecondNameCantBeNumberError,
    UserSecondNameLengthError
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class SecondName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, str):
            raise TypeError("Фамилия должна быть строчным типом")

        if self.value.isspace():
            raise UserSecondNameCantBeEmptyString("Фамилия пользователя не может быть пробелом")

        if self.value.isnumeric():
            raise UserSecondNameCantBeNumberError("Фамилия пользователя не может быть цифрами")

        if not 1 <= len(self.value) <= 255:
            raise UserSecondNameLengthError("Фамилия пользователя может быть в диапазоне от 1 до 255 символов")

    @override
    def __str__(self) -> str:
        return str(self.value)
