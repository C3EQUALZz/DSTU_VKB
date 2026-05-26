"""Порт чтения docx-контейнера — контракт для инфраструктуры."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)


@runtime_checkable
class DocxFormattingReader(Protocol):
    """Читает docx-контейнер и возвращает плоский список размеченных символов."""

    def read(self, path: Path) -> list[FormattedChar]:
        ...
