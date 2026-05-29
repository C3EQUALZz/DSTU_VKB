"""LsbEmbedder — встраивание байт сообщения в младшие биты каналов BMP.

Использует все три канала каждого пикселя последовательно (R → G → B),
обеспечивая максимальную плотность встраивания 3 бита на пиксель.
"""

from typing import final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    ContainerTooSmallError,
)


@final
class LsbEmbedder:
    """Записывает байты сообщения в LSB каналов изображения."""

    def embed(self, image: BmpImage, payload: bytes) -> BmpImage:
        bits = self._bytes_to_bits(payload)
        capacity = image.total_pixels * 3
        if len(bits) > capacity:
            raise ContainerTooSmallError(
                required_bits=len(bits),
                available_bits=capacity,
            )

        flat_pixels = list(image.flatten())
        for bit_index, bit in enumerate(bits):
            pixel_index, channel_index = divmod(bit_index, 3)
            flat_pixels[pixel_index] = _set_channel_lsb(
                flat_pixels[pixel_index], channel_index, bit,
            )
        return BmpImage.from_flat(image.width, image.height, flat_pixels)

    @staticmethod
    def _bytes_to_bits(payload: bytes) -> list[int]:
        return [
            (byte >> (7 - shift)) & 1
            for byte in payload
            for shift in range(8)
        ]


def _set_channel_lsb(pixel: Pixel, channel_index: int, bit: int) -> Pixel:
    if channel_index == 0:
        return pixel.with_red((pixel.red & ~1) | bit)
    if channel_index == 1:
        return pixel.with_green((pixel.green & ~1) | bit)
    return pixel.with_blue((pixel.blue & ~1) | bit)
