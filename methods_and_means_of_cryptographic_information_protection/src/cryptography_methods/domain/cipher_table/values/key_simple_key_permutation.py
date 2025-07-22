import re
from dataclasses import dataclass
from typing import Iterator

from typing_extensions import override

from cryptography_methods.domain.cipher_table.errors import (
    OnlyLettersCanBeInKeyError,
    StringContainsCharactersFromDifferentAlphabetsError
)
from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class KeyForSimpleKeyPermutation(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if not re.fullmatch(r'^[A-Za-zА-Яа-яЁё]+$', self.value, flags=re.UNICODE):
            raise OnlyLettersCanBeInKeyError("String must contains only letters")

        has_latin: bool = re.search(r'[A-Za-z]', self.value, flags=re.UNICODE) is not None
        has_cyrillic: bool = re.search(r'[А-Яа-яЁё]', self.value, flags=re.UNICODE) is not None

        if all(type_of_letters for type_of_letters in (has_cyrillic, has_latin)):
            raise StringContainsCharactersFromDifferentAlphabetsError(
                "String must contain only letters in same alphabet, not different"
            )

    @override
    def __str__(self) -> str:
        return str(self.value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.value)
