"""PixelSelector — псевдослучайный выбор N пикселей-носителей.

Использует детерминированный RNG (random.Random) с общим seed. Чтобы
обеспечить устойчивое извлечение, не выбираются пиксели на границах
изображения (где нет полного набора соседей для усреднения).
"""

from random import Random
from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage


@final
class PixelSelector:
    """Возвращает упорядоченный список координат (x, y) пикселей-носителей."""

    def __init__(self, seed: int) -> None:
        self._seed: Final[int] = seed

    def select(
        self, image: BmpImage, count: int, *, margin: int = 1,
    ) -> list[tuple[int, int]]:
        rng = Random(self._seed)  # noqa: S311
        candidates: list[tuple[int, int]] = [
            (x, y)
            for y in range(margin, image.height - margin)
            for x in range(margin, image.width - margin)
        ]
        rng.shuffle(candidates)
        return candidates[:count]
