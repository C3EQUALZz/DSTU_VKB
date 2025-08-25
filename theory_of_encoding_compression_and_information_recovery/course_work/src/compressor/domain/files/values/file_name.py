from dataclasses import dataclass

from typing_extensions import override

from compressor.domain.common.values.base import BaseValueObject
from compressor.domain.files.errors.file import FileNameIsEmptyError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class FileName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value.isspace() or self.value == '':
            msg: str = "file name must be provided, it cannot be empty"
            raise FileNameIsEmptyError(msg)

    @override
    def __str__(self) -> str:
        return self.value
