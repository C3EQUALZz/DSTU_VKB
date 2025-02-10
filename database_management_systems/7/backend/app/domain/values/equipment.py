import re
from dataclasses import dataclass
from typing import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import BadSerialNumberException


@dataclass(frozen=True)
class SerialNumber(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if not re.match(r'^[A-Za-z0-9]{5,20}$', self.value):
            raise BadSerialNumberException(self.value)

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
