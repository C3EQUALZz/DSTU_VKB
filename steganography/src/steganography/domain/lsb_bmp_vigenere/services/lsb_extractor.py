"""LsbExtractor — чтение байтов из младших битов каналов BMP."""

from typing import final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel


@final
class LsbExtractor:
    """Считывает поток байтов из LSB всех каналов изображения по порядку."""

    def extract(self, image: BmpImage, max_bytes: int | None = None) -> bytes:
        capacity_bits = image.total_pixels * 3
        wanted_bits = (
            min(capacity_bits, max_bytes * 8)
            if max_bytes is not None
            else capacity_bits - capacity_bits % 8
        )

        flat_pixels = image.flatten()
        bits: list[int] = []
        for bit_index in range(wanted_bits):
            pixel_index, channel_index = divmod(bit_index, 3)
            bits.append(_channel_lsb(flat_pixels[pixel_index], channel_index))

        out = bytearray()
        for byte_start in range(0, len(bits) - len(bits) % 8, 8):
            byte_value = 0
            for shift in range(8):
                byte_value = (byte_value << 1) | bits[byte_start + shift]
            out.append(byte_value)
        return bytes(out)


def _channel_lsb(pixel: Pixel, channel_index: int) -> int:
    if channel_index == 0:
        return pixel.red & 1
    if channel_index == 1:
        return pixel.green & 1
    return pixel.blue & 1
