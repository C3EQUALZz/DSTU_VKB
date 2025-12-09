from dataclasses import dataclass
from functools import total_ordering

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject


@total_ordering
@dataclass(frozen=True, unsafe_hash=True)
class FeedbackPositions(BaseValueObject):
    """Value Object для позиций обратной связи"""
    value: list[int]

    @override
    def _validate(self) -> None:
        if not self.value:
            raise ValueError("Должна быть указана хотя бы одна позиция обратной связи")

        if any(pos < 0 for pos in self.value):
            raise ValueError("Позиции не могут быть отрицательными")

    def __iter__(self):
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, FeedbackPositions):
            return False

        return self.value < other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, FeedbackPositions):
            return False

        return self.value > other.value

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FeedbackPositions):
            return False

        return self.value == other.value

    @override
    def __str__(self) -> str:
        return ", ".join(map(str, self.value))
