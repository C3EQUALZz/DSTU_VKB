"""Unit-тест полного цикла КДБ на синтетическом гладком изображении."""

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.kutter_jordan_bossen.services.kjb_embedder import (
    KjbEmbedder,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_extractor import (
    KjbExtractor,
)
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (
    LuminanceCalculator,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_parameters import (
    KjbParameters,
)


def _gradient_image(size: int = 32) -> BmpImage:
    return BmpImage.from_flat(
        width=size,
        height=size,
        flat=[
            Pixel(
                red=(x * 4) % 256,
                green=(y * 4) % 256,
                blue=((x + y) * 2) % 256,
            )
            for y in range(size) for x in range(size)
        ],
    )


def test_kjb_recovers_bits_on_smooth_image() -> None:
    image = _gradient_image()
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    params = KjbParameters(lambda_factor=0.3, seed=7)

    stego, stats = KjbEmbedder(luminance=LuminanceCalculator()).embed(
        image, bits, params,
    )
    extracted = KjbExtractor().extract(stego, bit_count=len(bits), params=params)

    assert extracted == bits
    assert stats.payload_bits == len(bits)
