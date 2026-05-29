"""Запись BMP через Pillow."""

from pathlib import Path

from PIL import Image

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.bmp_writer import BmpWriter


class PillowBmpWriter(BmpWriter):
    """Сохраняет BmpImage в BMP-файл (24-бит RGB)."""

    def write(self, image: BmpImage, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        flat_rgb = [
            (pixel.red, pixel.green, pixel.blue)
            for pixel in image.flatten()
        ]
        target = Image.new("RGB", (image.width, image.height))
        target.putdata(flat_rgb)
        target.save(path, format="BMP")
