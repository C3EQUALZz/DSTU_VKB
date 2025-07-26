import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, overload, Iterator, Final

from typing_extensions import override

from cryptography_methods.domain.cipher_table.errors import CantFindSymbolInTableError
from cryptography_methods.domain.cipher_table.values.table_dimension import TableDimension
from cryptography_methods.domain.cipher_table.values.table_id import TableID
from cryptography_methods.domain.common.entities.base_entity import BaseEntity

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True, repr=False)
class Table(BaseEntity[TableID]):
    width: TableDimension
    height: TableDimension
    data: list[list[str]] = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.data: list[list[str]] = [["" for _ in range(self.width)] for _ in range(self.height)]

    def __iter__(self) -> Iterator[list[str]]:
        """Возвращает итератор по строкам таблицы"""
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    @overload
    def __getitem__(self, index: int) -> list[str]:
        ...

    @overload
    def __getitem__(self, index: tuple[int, int]) -> str:
        ...

    def __getitem__(self, index: int | tuple[int, int]) -> list[str] | str:
        if isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError("Table index must be a tuple of two integers (row, col)")
            row, col = index
            return self.data[row][col]
        else:
            return self.data[index]

    @overload
    def __setitem__(self, index: tuple[int, int], value: str) -> None:
        ...

    @overload
    def __setitem__(self, index: int, value: list[str]) -> None:
        ...

    def __setitem__(self, index: int | tuple[int, int], value: Sequence[str]) -> None:
        if isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError("Table index must be a tuple of two integers (row, col)")
            row, col = index
            if not isinstance(value, str):
                raise TypeError("Cell value must be a string")
            self.data[row][col] = value
        else:
            if not isinstance(value, (list, tuple)):
                raise TypeError("Row value must be a list or tuple of strings")
            if len(value) != self.width.value:
                raise ValueError(f"Row must contain exactly {self.width.value} elements")
            self.data[index] = list(value)

    @override
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Table):
            return False

        return self.data == other.data

    @override
    def __str__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self.data)

    @override
    def __repr__(self) -> str:
        return f"Table(width={self.width}, height={self.height}, data={self.data})"

    def find(self, char: str) -> tuple[int, int]:
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == char:
                    logger.info(
                        "Successfully found char: %s at index row=%s, column=%s",
                        char, i, j
                    )
                    return i, j
        raise CantFindSymbolInTableError(f"Cant find symbol {char} in table")
