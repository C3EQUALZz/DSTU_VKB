from dataclasses import dataclass
from typing import override

from compressor.domain.common.values.base import BaseValueObject
from compressor.domain.users.constants import PASSWORD_MIN_LEN
from compressor.domain.users.errors import SmallPasswordLength


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class UserPasswordHash(BaseValueObject):
    value: bytes

    @override
    def _validate(self) -> None:
        if len(self.value) <= PASSWORD_MIN_LEN:
            msg: str = f"Password must be at least {PASSWORD_MIN_LEN} characters long."
            raise SmallPasswordLength(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
