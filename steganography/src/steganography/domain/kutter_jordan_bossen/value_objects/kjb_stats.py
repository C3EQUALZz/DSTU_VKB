"""KjbStats — характеристики выполненного встраивания КДБ."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KjbStats:
    """Сколько бит встроено, на сколько пикселей рассчитан контейнер."""

    payload_bits: int
    container_pixels: int

    @property
    def rate(self) -> float:
        return (
            self.payload_bits / self.container_pixels
            if self.container_pixels
            else 0.0
        )
