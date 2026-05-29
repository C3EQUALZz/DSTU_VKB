"""LsbReplacementMethod — классическая LSB-R с задаваемым шагом каналов."""

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
class LsbReplacementMethod:
    """LSB-R: бит сообщения заменяет младший бит выбранного канала.

    Параметр ``step`` задаёт шаг между задействованными каналами:
    ``step=1`` — каждый канал (максимальный рейт 1 бит/канал),
    ``step=4`` — каждый четвёртый канал (рейт 0.25 бит/канал) и т.п.
    """

    def __init__(self, channel_stream: ChannelStream) -> None:
        self._channels: Final[ChannelStream] = channel_stream

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
            new_value = (channels[channel_index] & ~1) | bit
            if new_value != channels[channel_index]:
                changed += 1
            channels[channel_index] = new_value
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
