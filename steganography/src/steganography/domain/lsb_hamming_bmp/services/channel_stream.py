"""ChannelStream — плоский поток байтов каналов BMP-изображения (R,G,B,R,…).

Сервис помогает методам встраивания работать единообразно: индексом
обращаться к любому каналу любого пикселя; собирать изменённый поток
обратно в BmpImage.
"""

from typing import final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel


@final
class ChannelStream:
    """Преобразование BmpImage ↔ list[int] (8-битные каналы)."""

    def to_channels(self, image: BmpImage) -> list[int]:
        channels: list[int] = []
        for pixel in image.flatten():
            channels.append(pixel.red)
            channels.append(pixel.green)
            channels.append(pixel.blue)
        return channels

    def from_channels(
        self, channels: list[int], width: int, height: int,
    ) -> BmpImage:
        expected = width * height * 3
        if len(channels) != expected:
            msg = f"ожидалось {expected} каналов, получено {len(channels)}"
            raise ValueError(msg)
        pixels: list[Pixel] = [
            Pixel(
                red=channels[offset],
                green=channels[offset + 1],
                blue=channels[offset + 2],
            )
            for offset in range(0, len(channels), 3)
        ]
        return BmpImage.from_flat(width=width, height=height, flat=pixels)
