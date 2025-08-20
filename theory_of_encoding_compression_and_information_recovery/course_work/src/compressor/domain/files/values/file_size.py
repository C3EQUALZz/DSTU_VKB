from dataclasses import dataclass
from typing import Self
from typing_extensions import override

from compressor.domain.common.values.base import BaseValueObject
from compressor.domain.files.entities.compressed_file import CompressedFile
from compressor.domain.files.errors.file import FileSizeNegativeError


@dataclass(frozen=True, unsafe_hash=True)
class FileSize(BaseValueObject):
    value: float

    @override
    def _validate(self) -> None:
        if self.value <= 0:
            raise FileSizeNegativeError("File size cannot be less than zero")

    @override
    def __str__(self) -> str:
        return str(self.value)

    def __ge__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value >= other.size.value

        if isinstance(other, (int, float)):
            return self.value >= other

        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value <= other.size.value

        if isinstance(other, (int, float)):
            return self.value <= other

        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value == other.size.value

        if isinstance(other, int):
            return self.value == other

        if isinstance(other, float):
            return self.value == round(other, 0)

        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value != other.size.value

        if isinstance(other, int):
            return self.value != other

        if isinstance(other, float):
            return self.value != round(other, 0)

        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value > other.size.value

        if isinstance(other, (int, float)):
            return self.value > other

        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, CompressedFile):
            return self.value < other.size.value
        if isinstance(other, (int, float)):
            return self.value < other
        return False

    def __truediv__(self, other: object) -> Self:
        if isinstance(other, CompressedFile):
            return FileSize(self.value / other.size.value)

        if isinstance(other, (int, float)):
            if round(other, 0) == 0:
                msg: str = "Cannot divide by zero"
                raise ZeroDivisionError(msg)
            return FileSize(self.value / other)

        msg: str = f"unsupported operand type(s) for /: 'FileSize' and '{type(other).__name__}'"

        raise TypeError(msg)
