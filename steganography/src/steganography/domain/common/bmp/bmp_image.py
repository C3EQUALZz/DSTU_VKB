"""BmpImage — агрегат BMP-изображения как двумерной сетки пикселей."""

from dataclasses import dataclass

from steganography.domain.common.bmp.pixel import Pixel


@dataclass(frozen=True, slots=True)
class BmpImage:
    """24-битное RGB-изображение фиксированной ширины и высоты."""

    width: int
    height: int
    pixels: tuple[tuple[Pixel, ...], ...]

    @property
    def total_pixels(self) -> int:
        return self.width * self.height

    def flatten(self) -> tuple[Pixel, ...]:
        """Развёрнутый порядок пикселей: строка за строкой."""
        return tuple(p for row in self.pixels for p in row)

    @classmethod
    def from_flat(
        cls, width: int, height: int, flat: list[Pixel],
    ) -> BmpImage:
        if len(flat) != width * height:
            msg = (
                f"длина flat ({len(flat)}) не равна width*height ({width * height})"
            )
            raise ValueError(msg)
        rows: list[tuple[Pixel, ...]] = []
        for row_index in range(height):
            start = row_index * width
            rows.append(tuple(flat[start : start + width]))
        return cls(width=width, height=height, pixels=tuple(rows))
