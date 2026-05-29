"""LuminanceCalculator — расчёт яркости пикселя по стандарту BT.601.

Используется формула ``Y = 0.299·R + 0.587·G + 0.114·B`` — компромисс
между точностью восприятия и простотой вычислений. Яркость определяет
амплитуду модуляции синего канала: ``ΔB = ±λ·Y``.
"""

from typing import Final, final

from steganography.domain.common.bmp.pixel import Pixel

_R_WEIGHT: Final[float] = 0.299
_G_WEIGHT: Final[float] = 0.587
_B_WEIGHT: Final[float] = 0.114


@final
class LuminanceCalculator:
    """Считает яркость по стандарту BT.601."""

    def of(self, pixel: Pixel) -> float:
        return (
            _R_WEIGHT * pixel.red
            + _G_WEIGHT * pixel.green
            + _B_WEIGHT * pixel.blue
        )
