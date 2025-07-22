from dataclasses import dataclass
from typing import Self, Iterator
from functools import total_ordering
from typing_extensions import override

from cryptography_methods.domain.cipher_table.errors import NegativeTableDimensionError, ZeroTableDimensionError
from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, eq=False, unsafe_hash=True)
@total_ordering
class TableDimension(BaseValueObject):
    value: int

    @override
    def _validate(self) -> None:
        if self.value < 0:
            raise NegativeTableDimensionError("Значение размера таблицы не может быть меньше 0")

        if self.value == 0:
            raise ZeroTableDimensionError("Значение размера таблицы не может быть равно 0")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, TableDimension):
            return self.value == other.value

        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value < other

        if isinstance(other, TableDimension):
            return self.value < other.value

        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value <= other

        if isinstance(other, TableDimension):
            return self.value <= other.value

        return False

    @override
    def __str__(self) -> str:
        return str(self.value)

    def __index__(self) -> int:
        return self.value

    def __int__(self) -> int:
        return self.value

    def __mul__(self, other: object) -> Self:
        if isinstance(other, int):
            return TableDimension(self.value * other)

        if isinstance(other, TableDimension):
            return TableDimension(self.value * other.value)

        raise NotImplementedError(
            f"Not implemented поддержки for multiply with this type: {type(other)},"
            f" please use int or TableDimension"
        )

    def __rmul__(self, other: object) -> Self:
        return self.__mul__(other)

    def __add__(self, other: object) -> Self:
        if isinstance(other, int):
            return TableDimension(self.value + other)

        if isinstance(other, TableDimension):
            return TableDimension(self.value + other.value)

        raise NotImplementedError(
            f"Not implemented поддержки for multiply with this type: {type(other)},"
            f" please use int or TableDimension"
        )

    def __radd__(self, other: object) -> Self:
        return self.__add__(other)

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.value))

    def __len__(self) -> int:
        return self.value

    @property
    def raw_value(self) -> int:
        return self.value
