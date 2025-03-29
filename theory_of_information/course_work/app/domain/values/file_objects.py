from dataclasses import dataclass

from typing_extensions import override

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import UnSupportedTypeOfFileException


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
        try:
            int(self.value)
        except ValueError:
            ...

        if int(self.value) < 0:
            ...

    @override
    def as_generic_type(self) -> str:
        units: tuple[str, str, str, str] = ('KB', 'MB', 'GB', 'TB')
        size_list: list[str] = [f'{int(self.value):,} B'] + [
            f'{int(self.value) / 1024 ** (i + 1):,.1f*} {u}' for i, u in
            enumerate(units)
        ]
        return [size for size in size_list if not size.startswith('0.')][-1]


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
