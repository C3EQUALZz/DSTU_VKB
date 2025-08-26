import re
from dataclasses import dataclass
from typing import override

from compressor.domain.common.values.base import BaseValueObject
from compressor.domain.users.constants import (
    PATTERN_ALLOWED_CHARS,
    PATTERN_END,
    PATTERN_NO_CONSECUTIVE_SPECIALS,
    PATTERN_START,
    USERNAME_MAX_LEN,
    USERNAME_MIN_LEN,
)
from compressor.domain.users.errors import UsernameError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Username(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if len(self.value) < USERNAME_MIN_LEN or len(self.value) > USERNAME_MAX_LEN:
            msg: str = (
                f"Username must be between "
                f"{USERNAME_MIN_LEN} and "
                f"{USERNAME_MAX_LEN} characters."
            )

            raise UsernameError(msg)

        if not re.match(PATTERN_START, self.value):
            msg: str = "Username must start with a letter (A-Z, a-z, А-Я, а-я) or a digit (0-9)."
            raise UsernameError(msg)

        if not re.fullmatch(PATTERN_ALLOWED_CHARS, self.value):
            msg: str = (
                "Username can only contain letters (A-Z, a-z, А-Я, а-я), digits (0-9), "
                "dots (.), hyphens (-), and underscores (_)."
            )

            raise UsernameError(msg)

        if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, self.value):
            msg: str = (
                "Username cannot contain consecutive special characters"
                " like .., --, or __."
            )

            raise UsernameError(msg)

        if not re.match(PATTERN_END, self.value):
            msg: str = (
                "Username must end with a letter (A-Z, a-z, А-Я, а-я) or a digit (0-9)."
            )

            raise UsernameError(msg)

    @override
    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)
