"""KjbExtractor — извлечение бит из синего канала по методу КДБ.

Для каждого пикселя-носителя вычисляется среднее значение синего
канала по крестообразной окрестности (4 соседа на ``radius=1``).
Если синий пикселя больше среднего → бит «1», иначе → «0».
"""

from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.kutter_jordan_bossen.services.pixel_selector import (
    PixelSelector,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_parameters import (
    KjbParameters,
)


@final
class KjbExtractor:
    """Извлечение скрытых бит из BMP с известными параметрами КДБ."""

    def __init__(
        self,
        selector_factory: type[PixelSelector] = PixelSelector,
    ) -> None:
        self._selector_factory: Final[type[PixelSelector]] = selector_factory

    def extract(
        self,
        image: BmpImage,
        bit_count: int,
        params: KjbParameters,
    ) -> list[int]:
        selector = self._selector_factory(params.seed)
        positions = selector.select(
            image, count=bit_count, margin=params.neighbour_radius,
        )
        result: list[int] = []
        for x, y in positions:
            expected_blue = self._average_neighbour_blue(
                image, x, y, params.neighbour_radius,
            )
            actual_blue = image.pixels[y][x].blue
            result.append(1 if actual_blue > expected_blue else 0)
        return result

    @staticmethod
    def _average_neighbour_blue(
        image: BmpImage, x: int, y: int, radius: int,
    ) -> float:
        total = 0
        count = 0
        for offset in range(-radius, radius + 1):
            if offset == 0:
                continue
            if 0 <= x + offset < image.width:
                total += image.pixels[y][x + offset].blue
                count += 1
            if 0 <= y + offset < image.height:
                total += image.pixels[y + offset][x].blue
                count += 1
        return total / count if count else 0.0
