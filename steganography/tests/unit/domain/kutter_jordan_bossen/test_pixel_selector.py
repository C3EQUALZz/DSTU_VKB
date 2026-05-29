"""Тесты псевдослучайного выбора пикселей-носителей."""

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.kutter_jordan_bossen.services.pixel_selector import (
    PixelSelector,
)


def _flat_image(width: int, height: int) -> BmpImage:
    return BmpImage.from_flat(
        width=width,
        height=height,
        flat=[Pixel(red=100, green=100, blue=100)] * (width * height),
    )


def test_selector_is_deterministic_for_same_seed() -> None:
    image = _flat_image(10, 10)
    first = PixelSelector(seed=42).select(image, count=20)
    second = PixelSelector(seed=42).select(image, count=20)
    assert first == second


def test_selector_changes_with_seed() -> None:
    image = _flat_image(10, 10)
    first = PixelSelector(seed=1).select(image, count=20)
    second = PixelSelector(seed=2).select(image, count=20)
    assert first != second


def test_selector_respects_margin() -> None:
    image = _flat_image(8, 8)
    positions = PixelSelector(seed=0).select(image, count=10, margin=1)
    for x, y in positions:
        assert 1 <= x < 7
        assert 1 <= y < 7
