"""Тесты LSB-вставки/извлечения байтов в каналах BMP."""

import pytest

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    ContainerTooSmallError,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_embedder import (
    LsbEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_extractor import (
    LsbExtractor,
)


def _solid_image(width: int, height: int) -> BmpImage:
    return BmpImage.from_flat(
        width=width,
        height=height,
        flat=[Pixel(red=100, green=100, blue=100)] * (width * height),
    )


def test_embed_then_extract_roundtrip() -> None:
    image = _solid_image(8, 8)
    payload = b"\xaa\x55\xff\x00"

    embedded = LsbEmbedder().embed(image, payload)
    extracted = LsbExtractor().extract(embedded, max_bytes=len(payload))

    assert extracted == payload


def test_embed_raises_when_capacity_exceeded() -> None:
    image = _solid_image(2, 2)  # 12 LSB-бит
    too_big = b"\x00" * 4  # 32 бита

    with pytest.raises(ContainerTooSmallError):
        LsbEmbedder().embed(image, too_big)
