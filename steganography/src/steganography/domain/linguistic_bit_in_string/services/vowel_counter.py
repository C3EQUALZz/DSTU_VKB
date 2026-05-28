"""VowelCounter — считает русские гласные в строке.

Гласные русского алфавита: А, Е, Ё, И, О, У, Ы, Э, Ю, Я (в любом регистре).
"""

from typing import Final


class VowelCounter:
    """Сервис подсчёта гласных в строке."""

    _VOWELS: Final[frozenset[str]] = frozenset("аеёиоуыэюя")

    def count(self, text: str) -> int:
        return sum(1 for ch in text.lower() if ch in self._VOWELS)
