"""Порт записи BMP-файла."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.common.bmp.bmp_image import BmpImage


@runtime_checkable
class BmpWriter(Protocol):
    """Сохраняет BmpImage в файл."""

    def write(self, image: BmpImage, path: Path) -> None:
        ...
