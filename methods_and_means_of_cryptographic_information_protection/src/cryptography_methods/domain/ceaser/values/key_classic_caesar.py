from dataclasses import dataclass
from typing import Iterator

from typing_extensions import override

from cryptography_methods.domain.ceaser.errors import (
    NegativeKeyForClassicCaesarError,
    UnknownAlphabetError,
    BadKeyForClassicCaesarError
)
from cryptography_methods.domain.common.values import BaseValueObject
from cryptography_methods.domain.common.values.languages import LanguageType


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class KeyClassicCaesar(BaseValueObject):
    """
    Ключом шифрования является целое число 1 … N, где N – количество букв алфавита шифруемого слова, уменьшенное на 1.
    Ключ будет обозначаться символом К.
    """
    value: int
    alphabet: LanguageType

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, int):
            raise TypeError("Value must be a integer")

        if self.value <= 0:
            raise NegativeKeyForClassicCaesarError("Value must be a positive integer")

        count_of_symbols_in_alphabet: int

        if self.alphabet is LanguageType.RUSSIAN:
            count_of_symbols_in_alphabet = 33
        elif self.alphabet is LanguageType.ENGLISH:
            count_of_symbols_in_alphabet = 26
        else:
            raise UnknownAlphabetError("Unknown alphabet, you forgot to add code here")

        if not self.value <= count_of_symbols_in_alphabet - 1:
            raise BadKeyForClassicCaesarError("Value must be lower than length of alphabet - 1")

    def __index__(self) -> int:
        return self.value

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.value))

    @override
    def __str__(self) -> str:
        return str(self.value)
