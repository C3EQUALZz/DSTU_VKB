"""Pixel — RGB-тройка пикселя BMP-изображения."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pixel:
    """Один пиксель: каналы red/green/blue в диапазоне 0–255."""

    red: int
    green: int
    blue: int

    def with_blue(self, value: int) -> Pixel:
        return Pixel(red=self.red, green=self.green, blue=value)

    def with_red(self, value: int) -> Pixel:
        return Pixel(red=value, green=self.green, blue=self.blue)

    def with_green(self, value: int) -> Pixel:
        return Pixel(red=self.red, green=value, blue=self.blue)
