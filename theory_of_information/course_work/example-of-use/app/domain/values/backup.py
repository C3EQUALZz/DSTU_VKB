from dataclasses import dataclass

from app.domain.values.base import BaseValueObject
from typing_extensions import override


@dataclass
class CompressionType(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        if self.value not in ("gzip", "bzip2"):
            raise

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
