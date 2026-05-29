"""Порт чтения BMP-файла."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.common.bmp.bmp_image import BmpImage


@runtime_checkable
class BmpReader(Protocol):
    """Читает BMP-файл и возвращает агрегат BmpImage."""

    def read(self, path: Path) -> BmpImage:
        ...
