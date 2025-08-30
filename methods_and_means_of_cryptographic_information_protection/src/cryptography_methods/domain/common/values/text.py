import logging
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self, Final

from typing_extensions import override

from cryptography_methods.domain.common.errors.text import (
    TextCantContainsDigitsError,
    StringContainsMultipleLanguagesError
)
from cryptography_methods.domain.common.values import BaseValueObject

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Text(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value is None or not isinstance(self.value, str):
            raise TypeError(f"Value {self.value} is not a string")

        if re.search(r"\d", self.value):
            raise TextCantContainsDigitsError("text can't contain digits")

        has_english: bool = bool(re.search(r'[a-zA-Z]', self.value))
        has_russian: bool = bool(re.search(r'[а-яА-Я]', self.value))

        if all(language for language in (has_english, has_russian)):
            raise StringContainsMultipleLanguagesError(f"{self.value} contains multiple languages")

    def __iter__(self) -> Iterator[str]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    @override
    def __str__(self) -> str:
        return str(self.value)

    def __getitem__(self, index: int) -> str:
        return self.value[index]

    def lower(self) -> Self:
        lowered_text: str = self.value.lower()
        logger.info(
            "Called lowering for symbols, original text: %s, lowered text: %s",
            self.value,
            lowered_text
        )
        return Text(lowered_text)

    def upper(self) -> Self:
        uppercased_text: str = self.value.upper()
        logger.info(
            "Called uppercasing for symbols, original text: %s, uppercased text: %s",
            self.value,
            uppercased_text
        )
        return Text(uppercased_text)

    def islower(self) -> bool:
        return self.value.islower()

    def isupper(self) -> bool:
        return self.value.isupper()
