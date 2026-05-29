"""Фабрики тестовых BMP-файлов для интеграционных тестов."""

import random
from pathlib import Path

from PIL import Image


def build_random_bmp(
    path: Path, width: int, height: int, *, seed: int = 0,
) -> Path:
    """Создать BMP с псевдослучайными RGB-пикселями (детерминированно)."""
    rng = random.Random(seed)  # noqa: S311
    image = Image.new("RGB", (width, height))
    image.putdata(
        [
            (
                rng.randint(0, 255),
                rng.randint(0, 255),
                rng.randint(0, 255),
            )
            for _ in range(width * height)
        ],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="BMP")
    return path
