from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from typing_extensions import override

from cryptography_methods.domain.common.errors.time_errors import (
    DeleteTimeFormatError,
    DeleteTimeFutureError,
)
from cryptography_methods.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class DeleteTime(BaseValueObject):
    value: datetime | None

    @override
    def _validate(self) -> None:
        """
        Check that a value is valid to create this value object.
        """
        if self.value is None:
            return

        if self.value.tzinfo != UTC:
            raise DeleteTimeFormatError(
                f"DeleteTime must be timezone-aware with UTC, "
                f"not this: {self.value.tzinfo!s}",
            )

        if self.value > datetime.now(UTC):
            raise DeleteTimeFutureError("DeleteTime cannot be in the future")

    @override
    def __str__(self) -> str:
        if self.value is None:
            return ""
        return self.value.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def create_deleted(cls) -> Self:
        return cls(datetime.now(UTC))

    @classmethod
    def create_not_deleted(cls) -> Self:
        return cls(None)

    @property
    def is_deleted(self) -> bool:
        return self.value is not None