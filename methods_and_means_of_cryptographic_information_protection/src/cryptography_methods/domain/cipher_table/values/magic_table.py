from dataclasses import dataclass

from typing_extensions import override

from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class MagicTable(BaseValueObject):
    value: list[list[int]]

    @override
    def _validate(self) -> None:
        for row in self.value:
            for num in row:
                if num <= 0:
                    raise ValueError("Magic table must have positive numbers only!")

    @override
    def __str__(self) -> str:
        return '\n'.join((' '.join(map(str, row)) for row in self.value))

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index: int) -> list[int]:
        return self.value[index]

    @property
    def width(self) -> int:
        return len(self.value[0])

    @property
    def height(self) -> int:
        return len(self.value)
