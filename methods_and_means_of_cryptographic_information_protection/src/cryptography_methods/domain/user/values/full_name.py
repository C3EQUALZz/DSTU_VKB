from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject
from cryptography_methods.domain.user.values import first_name
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class FullName(BaseValueObject):
    first_name: str
    second_name: str
    middle_name: str

    @override
    def _validate(self) -> None:
        _ = FirstName(self.first_name)
        _ = SecondName(self.second_name)
        _ = MiddleName(self.middle_name)

    @override
    def __str__(self) -> str:
        return f"{first_name} {self.middle_name} {self.second_name}"
