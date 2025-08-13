from collections import deque
from dataclasses import dataclass
from typing import Iterator

from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, unsafe_hash=True)
class RegisterState(BaseValueObject):
    value: deque[int]

    def _validate(self) -> None:
        if not self.value:
            raise ValueError("Состояние регистра не может быть пустым")

        if not all(bit in (0, 1) for bit in self.value):
            raise ValueError("Все биты состояния должны быть 0 или 1")

    def pop(self) -> int:
        return self.value.pop()

    def append_left(self, bit: int) -> None:
        self.value.appendleft(bit)

    def __iter__(self) -> Iterator[int]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RegisterState):
            return False

        return self.value == other.value

    def __str__(self) -> str:
        return ''.join(map(str, self.value))
