import re
from dataclasses import dataclass
from typing import override
from app.domain.values.base import BaseValueObject
from app.exceptions.domain import BadFormatNumberException, HumanBadFullNameComponentException


@dataclass(frozen=True)
class HumanFullNameComponent(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if not re.match(r'^[A-Za-zА-Яа-яёЁ-]+$', self.value):
            raise HumanBadFullNameComponentException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PhoneNumber(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if not re.match(r'^(\+7|8)[0-9]{10}$', self.value):
            raise BadFormatNumberException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value
