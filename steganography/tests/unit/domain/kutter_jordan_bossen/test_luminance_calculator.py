"""Тесты расчёта яркости BT.601."""

import pytest

from steganography.domain.common.bmp.pixel import Pixel
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (
    LuminanceCalculator,
)


@pytest.mark.parametrize(
    ("red", "green", "blue", "expected"),
    [
        (255, 255, 255, 255.0),
        (0, 0, 0, 0.0),
        (255, 0, 0, 76.245),
        (0, 255, 0, 149.685),
        (0, 0, 255, 29.07),
    ],
)
def test_luminance(red: int, green: int, blue: int, expected: float) -> None:
    pixel = Pixel(red=red, green=green, blue=blue)
    assert LuminanceCalculator().of(pixel) == pytest.approx(expected, abs=0.01)
