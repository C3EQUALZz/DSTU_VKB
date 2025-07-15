from cryptography_methods.domain.common.values import BaseValueObject
from dataclasses import dataclass
from typing_extensions import override


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class UserName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, str):
            raise TypeError("Юзернейм пользователя может быть только типом str")

    @override
    def __str__(self) -> str:
        return str(self.value)
