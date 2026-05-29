"""Фабрика гладких градиентных BMP — корректных тестовых контейнеров для КДБ."""

from pathlib import Path

from PIL import Image


def build_gradient_bmp(path: Path, width: int = 128, height: int = 128) -> Path:
    """Плавный градиент по R/G/B — соседи близки, КДБ работает корректно."""
    image = Image.new("RGB", (width, height))
    image.putdata(
        [
            (
                (x * 2) % 256,
                (y * 2) % 256,
                ((x + y) % 256),
            )
            for y in range(height) for x in range(width)
        ],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="BMP")
    return path
