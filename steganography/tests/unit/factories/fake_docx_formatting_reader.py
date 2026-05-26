"""In-memory реализация порта чтения docx для unit-тестов handler'ов."""

from pathlib import Path
from typing import final

from steganography.domain.text_format_decode.ports.docx_formatting_reader import (
    DocxFormattingReader,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)


@final
class FakeDocxFormattingReader(DocxFormattingReader):
    """Возвращает заранее заданный список символов, не читая файлы с диска."""

    def __init__(self, chars: list[FormattedChar]) -> None:
        self._chars = chars

    def read(self, path: Path) -> list[FormattedChar]:  # noqa: ARG002
        return self._chars
