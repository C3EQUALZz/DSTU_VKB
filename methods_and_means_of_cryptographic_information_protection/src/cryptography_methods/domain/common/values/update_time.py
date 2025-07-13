from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from typing_extensions import override

from cryptography_methods.domain.common.errors.time_errors import (
    UpdateTimeFormatError,
    UpdateTimeFutureError,
)
from cryptography_methods.domain.common.values.base import BaseValueObject


@dataclass(frozen=True)
class UpdateTime(BaseValueObject):
    value: datetime

    @override
    def _validate(self) -> None:
        if self.value.tzinfo != UTC:
            raise UpdateTimeFormatError(
                f"UpdateTime must be timezone-aware with UTC,"
                f" not this: {self.value.tzinfo!s}",
            )

        if self.value > datetime.now(UTC):
            raise UpdateTimeFutureError("UpdateTime cannot be in the future")

    @override
    def __str__(self) -> str:
        return self.value.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def now(cls) -> Self:
        return cls(datetime.now(UTC))
