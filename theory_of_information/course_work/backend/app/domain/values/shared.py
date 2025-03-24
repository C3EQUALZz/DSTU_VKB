from dataclasses import dataclass
from typing import override
from urllib.parse import urlparse

from app.domain.values.base import BaseValueObject
from app.exceptions.domain import URLMalformedException


@dataclass
class URL(BaseValueObject[str]):
    value: str

    @override
    def validate(self) -> None:
        try:
            result = urlparse(self.value)
            all([result.scheme, result.netloc])
        except AttributeError:
            raise URLMalformedException()

    @override
    def as_generic_type(self) -> str:
        return str(self.value)
