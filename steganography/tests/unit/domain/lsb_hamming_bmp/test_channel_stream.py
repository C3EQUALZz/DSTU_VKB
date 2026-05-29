"""Тесты конвертации BmpImage ↔ список каналов."""

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.lsb_hamming_bmp.services.channel_stream import (
    ChannelStream,
)


def test_channel_stream_roundtrip() -> None:
    image = BmpImage.from_flat(
        width=2,
        height=2,
        flat=[
            Pixel(red=10, green=20, blue=30),
            Pixel(red=40, green=50, blue=60),
            Pixel(red=70, green=80, blue=90),
            Pixel(red=100, green=110, blue=120),
        ],
    )
    stream = ChannelStream()

    channels = stream.to_channels(image)
    assert channels == [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
    ]
    rebuilt = stream.from_channels(channels, width=2, height=2)
    assert rebuilt == image
