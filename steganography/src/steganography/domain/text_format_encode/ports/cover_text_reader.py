"""Порт чтения текста-контейнера из источника (например, docx)."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)


@runtime_checkable
class CoverTextReader(Protocol):
    """Возвращает текст контейнера с сохранённой построчной структурой."""

    def read(self, path: Path) -> CoverText:
        ...
