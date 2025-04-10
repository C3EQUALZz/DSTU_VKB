import contextlib
from dataclasses import dataclass

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import UnSupportedTypeOfFileException
from typing_extensions import override


@dataclass
class TypeOfFile(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("file", "directory"):
            raise UnSupportedTypeOfFileException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class SizeOfFile(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        with contextlib.suppress(ValueError):
            int(self.value)

        if int(self.value) < 0:
            ...

    @override
    def as_generic_type(self) -> str:
        units: tuple[str, str, str, str] = ("KB", "MB", "GB", "TB")
        size_list: list[str] = [f"{int(self.value):,} B"] + [
            f"{int(self.value) / 1024 ** (i + 1):,.1f} {u}" for i, u in enumerate(units)
        ]
        return [size for size in size_list if not size.startswith("0.")][-1]


@dataclass
class PermissionsOfFile(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if len(self.value) != 3:
            ...

        if int(self.value) > 666:
            ...

    @override
    def as_generic_type(self) -> str:
        return self.value
