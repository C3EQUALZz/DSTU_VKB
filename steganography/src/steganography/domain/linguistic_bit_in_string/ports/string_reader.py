"""Порт чтения строк-кандидатов из источника (файл, stdin)."""

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class StringReader(Protocol):
    """Читает источник и возвращает список строк (по одной на запись)."""

    def read(self, path: Path) -> list[str]:
        ...
