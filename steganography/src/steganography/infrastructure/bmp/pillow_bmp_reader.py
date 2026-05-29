"""Чтение BMP через Pillow."""

from pathlib import Path

from PIL import Image

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.common.bmp.pixel import Pixel


class PillowBmpReader(BmpReader):
    """Загружает BMP-файл и собирает агрегат BmpImage."""

    def read(self, path: Path) -> BmpImage:
        with Image.open(path) as raw_image:
            converted = raw_image.convert("RGB")
            width, height = converted.size
            raw_pixels = list(converted.getdata())
        flat = [
            Pixel(red=red, green=green, blue=blue)
            for red, green, blue in raw_pixels
        ]
        return BmpImage.from_flat(width=width, height=height, flat=flat)
