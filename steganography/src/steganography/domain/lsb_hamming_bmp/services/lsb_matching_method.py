"""LsbMatchingMethod — мягкий вариант LSB: при несовпадении ±1 вместо замены.

LSB-M статистически устойчивее LSB-R: распределение значений каналов
после внедрения остаётся сглаженным, что затрудняет стегоанализ по
гистограмме. Извлечение симметрично LSB-R: бит = LSB канала.
"""

from random import Random
from typing import Final, final

from steganography.domain.common.bmp.bmp_image import BmpImage
from steganography.domain.lsb_hamming_bmp.errors.embedding_errors import (
    ContainerTooSmallError,
)
from steganography.domain.lsb_hamming_bmp.services.channel_stream import (
    ChannelStream,
)
from steganography.domain.lsb_hamming_bmp.value_objects.embedding_stats import (
    EmbeddingStats,
)


@final
class LsbMatchingMethod:
    """LSB-M с задаваемым шагом каналов и детерминированным RNG."""

    def __init__(
        self, channel_stream: ChannelStream, *, seed: int = 0,
    ) -> None:
        self._channels: Final[ChannelStream] = channel_stream
        self._rng: Final[Random] = Random(seed)  # noqa: S311

    def embed(
        self, image: BmpImage, bits: list[int], step: int,
    ) -> tuple[BmpImage, EmbeddingStats]:
        channels = self._channels.to_channels(image)
        positions = list(range(0, len(channels), max(step, 1)))
        if len(bits) > len(positions):
            raise ContainerTooSmallError(
                required=len(bits), available=len(positions),
            )
        changed = 0
        for index, bit in enumerate(bits):
            channel_index = positions[index]
            old_value = channels[channel_index]
            new_value = self._adjust(old_value, bit)
            channels[channel_index] = new_value
            if new_value != old_value:
                changed += 1
        new_image = self._channels.from_channels(
            channels, image.width, image.height,
        )
        stats = EmbeddingStats(
            payload_bits=len(bits),
            capacity_bits=len(positions),
            changed_channels=changed,
        )
        return new_image, stats

    def extract(
        self, image: BmpImage, bit_count: int, step: int,
    ) -> list[int]:
        channels = self._channels.to_channels(image)
        positions = list(range(0, len(channels), max(step, 1)))
        return [channels[positions[i]] & 1 for i in range(bit_count)]

    def _adjust(self, value: int, target_bit: int) -> int:
        if value & 1 == target_bit:
            return value
        if value == 0:
            return 1
        if value == 255:
            return 254
        return value + 1 if self._rng.random() < 0.5 else value - 1
