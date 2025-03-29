from dataclasses import dataclass

from app.domain.values.base import BaseValueObject
from typing_extensions import override

from app.exceptions.domain import UnsupportedFileObjectExtensionException


@dataclass
class CompressionType(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if not self.value.endswith(("gzip", "bzip2", "gz")):
            raise UnsupportedFileObjectExtensionException

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
