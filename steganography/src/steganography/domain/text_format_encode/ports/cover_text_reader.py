"""Порт чтения текста-контейнера из источника (например, docx)."""

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class CoverTextReader(Protocol):
    """Возвращает «голый» текст контейнера для последующего встраивания."""

    def read(self, path: Path) -> str:
        ...
