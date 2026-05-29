"""EmbeddingStats — характеристики выполненного встраивания."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmbeddingStats:
    """Сколько бит встроено, сколько LSB изменено, какая итоговая ёмкость."""

    payload_bits: int
    capacity_bits: int
    changed_channels: int

    @property
    def rate(self) -> float:
        return self.payload_bits / self.capacity_bits if self.capacity_bits else 0.0

    @property
    def distortion(self) -> float:
        if self.capacity_bits == 0:
            return 0.0
        return self.changed_channels / self.capacity_bits
