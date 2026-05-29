"""Тесты доменных методов LSB-R / LSB-M / Хемминг."""

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.lsb_hamming_bmp.services.channel_stream import (
    ChannelStream,
)
from steganography.domain.lsb_hamming_bmp.services.hamming_15_11_method import (
    Hamming15_11Method,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_matching_method import (
    LsbMatchingMethod,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_replacement_method import (
    LsbReplacementMethod,
)


def _image(width: int = 16, height: int = 16, fill: int = 128) -> BmpImage:
    return BmpImage.from_flat(
        width=width,
        height=height,
        flat=[Pixel(red=fill, green=fill, blue=fill)] * (width * height),
    )


def test_lsb_replacement_roundtrip() -> None:
    method = LsbReplacementMethod(channel_stream=ChannelStream())
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]
    image = _image()

    stego, stats = method.embed(image, bits, step=1)
    extracted = method.extract(stego, bit_count=len(bits), step=1)

    assert extracted == bits
    assert stats.payload_bits == len(bits)


def test_lsb_matching_roundtrip() -> None:
    method = LsbMatchingMethod(channel_stream=ChannelStream(), seed=7)
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    image = _image()

    stego, stats = method.embed(image, bits, step=2)
    extracted = method.extract(stego, bit_count=len(bits), step=2)

    assert extracted == bits
    assert stats.payload_bits == len(bits)


def test_hamming_15_11_roundtrip() -> None:
    method = Hamming15_11Method(channel_stream=ChannelStream())
    # 4 блока по 4 бита = 16 бит
    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    image = _image()

    stego, stats = method.embed(image, bits)
    extracted = method.extract(stego, bit_count=len(bits))

    assert extracted == bits
    # На блок Хемминга максимум 1 изменение из 15 каналов
    assert stats.changed_channels <= len(bits) // 4
