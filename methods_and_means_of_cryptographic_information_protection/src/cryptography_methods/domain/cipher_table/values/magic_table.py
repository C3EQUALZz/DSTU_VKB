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

        n = len(self.value)
        if n == 0:
            raise ValueError("Magic table cannot be empty!")

        for row in self.value:
            if len(row) != n:
                raise ValueError("Magic table must be square!")

        all_numbers = []
        for row in self.value:
            for num in row:
                if num <= 0:
                    raise ValueError("Magic table must have positive numbers only!")
                all_numbers.append(num)

        if sorted(all_numbers) != list(range(1, n * n + 1)):
            raise ValueError("Magic table must contain consecutive numbers from 1 to n*n!")

        magic_sum = n * (n * n + 1) // 2

        for i in range(n):
            if sum(self.value[i]) != magic_sum:
                raise ValueError(f"Row {i} sum is not equal to magic sum!")

        for j in range(n):
            if sum(self.value[i][j] for i in range(n)) != magic_sum:
                raise ValueError(f"Column {j} sum is not equal to magic sum!")

        if sum(self.value[i][i] for i in range(n)) != magic_sum:
            raise ValueError("Main diagonal sum is not equal to magic sum!")

        if sum(self.value[i][n - 1 - i] for i in range(n)) != magic_sum:
            raise ValueError("Secondary diagonal sum is not equal to magic sum!")

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
