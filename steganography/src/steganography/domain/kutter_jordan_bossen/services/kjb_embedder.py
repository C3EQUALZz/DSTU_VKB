"""KjbEmbedder — встраивание бит сообщения по методу Куттера-Джордана-Боссена.

Для каждого бита из псевдослучайно выбранного множества пикселей
синий канал модулируется на ``±λ·Y``: бит «1» → ``B'=B+λ·Y``, бит «0»
→ ``B'=B-λ·Y``. Значения насыщаются в диапазоне 0–255.
"""

from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.kutter_jordan_bossen.errors.kjb_errors import (
    ContainerTooSmallError,
)
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (
    LuminanceCalculator,
)
from steganography.domain.kutter_jordan_bossen.services.pixel_selector import (
    PixelSelector,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_parameters import (
    KjbParameters,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_stats import (
    KjbStats,
)


@final
class KjbEmbedder:
    """Встраивание битов сообщения в синий канал изображения."""

    def __init__(
        self,
        luminance: LuminanceCalculator,
        selector_factory: type[PixelSelector] = PixelSelector,
    ) -> None:
        self._luminance: Final[LuminanceCalculator] = luminance
        self._selector_factory: Final[type[PixelSelector]] = selector_factory

    def embed(
        self,
        image: BmpImage,
        bits: list[int],
        params: KjbParameters,
    ) -> tuple[BmpImage, KjbStats]:
        selector = self._selector_factory(params.seed)
        positions = selector.select(
            image, count=len(bits), margin=params.neighbour_radius,
        )
        if len(positions) < len(bits):
            raise ContainerTooSmallError(
                required=len(bits), available=len(positions),
            )

        rows = [list(row) for row in image.pixels]
        for (x, y), bit in zip(positions, bits, strict=True):
            old_pixel = rows[y][x]
            luminance = self._luminance.of(old_pixel)
            delta = params.lambda_factor * luminance
            new_blue = (
                old_pixel.blue + delta if bit == 1 else old_pixel.blue - delta
            )
            rows[y][x] = old_pixel.with_blue(_clamp_byte(round(new_blue)))

        new_image = BmpImage(
            width=image.width,
            height=image.height,
            pixels=tuple(tuple(row) for row in rows),
        )
        return new_image, KjbStats(
            payload_bits=len(bits),
            container_pixels=image.total_pixels,
        )


def _clamp_byte(value: int) -> int:
    if value < 0:
        return 0
    if value > 255:
        return 255
    return value
