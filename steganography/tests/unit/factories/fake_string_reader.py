"""In-memory реализация порта чтения строк для unit-тестов."""

from pathlib import Path
from typing import final

from steganography.domain.linguistic_bit_in_string.ports.string_reader import (
    StringReader,
)


@final
class FakeStringReader(StringReader):
    """Возвращает заранее заданный список строк, не трогая файловую систему."""

    def __init__(self, strings: list[str]) -> None:
        self._strings = strings

    def read(self, path: Path) -> list[str]:  # noqa: ARG002
        return self._strings
