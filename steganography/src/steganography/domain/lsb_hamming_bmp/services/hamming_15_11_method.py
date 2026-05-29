"""Hamming15_11Method — эффективное стег-кодирование с минимальными искажениями.

Идея: для группы из 15 LSB-битов контейнера ``c = (c1, …, c15)`` вычисляется
синдром ``s = H · c^T`` (4 бита), где H — проверочная матрица кода
Хемминга (15,11) (столбцы H — двоичные представления чисел 1..15).

Чтобы внедрить 4 бита сообщения ``m``, мы вычисляем
``i = (s XOR m)`` как индекс ``1..15`` (или 0 — тогда ничего не меняем) и
инвертируем ровно один бит ``c[i]``. После этого новый синдром равен
``m``, что и читает приёмник.

Рейт встраивания: 4 бита / 15 каналов ≈ 0.267 бит/канал. При этом
искажается не более одного LSB на группу — против 4 LSB при обычном
LSB-R при том же объёме внедрения.
"""

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

_BLOCK_SIZE: Final[int] = 15
_PAYLOAD_BITS_PER_BLOCK: Final[int] = 4


@final
class Hamming15_11Method:  # noqa: N801
    """Встраивание блоками по 15 каналов; на блок — 4 бита сообщения."""

    def __init__(self, channel_stream: ChannelStream) -> None:
        self._channels: Final[ChannelStream] = channel_stream

    def embed(
        self, image: BmpImage, bits: list[int],
    ) -> tuple[BmpImage, EmbeddingStats]:
        channels = self._channels.to_channels(image)
        block_count = len(channels) // _BLOCK_SIZE
        capacity_bits = block_count * _PAYLOAD_BITS_PER_BLOCK
        if len(bits) > capacity_bits:
            raise ContainerTooSmallError(
                required=len(bits), available=capacity_bits,
            )

        changed = 0
        for block_index, payload_offset in enumerate(
            range(0, len(bits), _PAYLOAD_BITS_PER_BLOCK),
        ):
            payload_nibble = bits[
                payload_offset : payload_offset + _PAYLOAD_BITS_PER_BLOCK
            ]
            if len(payload_nibble) < _PAYLOAD_BITS_PER_BLOCK:
                payload_nibble = payload_nibble + [0] * (
                    _PAYLOAD_BITS_PER_BLOCK - len(payload_nibble)
                )
            block_start = block_index * _BLOCK_SIZE
            block_lsb = [
                channels[block_start + i] & 1 for i in range(_BLOCK_SIZE)
            ]
            syndrome = _syndrome(block_lsb)
            target_index = _xor_int(syndrome, _bits_to_int(payload_nibble))
            if target_index != 0:
                channel_index = block_start + target_index - 1
                channels[channel_index] ^= 1
                changed += 1

        new_image = self._channels.from_channels(
            channels, image.width, image.height,
        )
        stats = EmbeddingStats(
            payload_bits=len(bits),
            capacity_bits=capacity_bits,
            changed_channels=changed,
        )
        return new_image, stats

    def extract(self, image: BmpImage, bit_count: int) -> list[int]:
        channels = self._channels.to_channels(image)
        out: list[int] = []
        block_index = 0
        while len(out) < bit_count:
            block_start = block_index * _BLOCK_SIZE
            if block_start + _BLOCK_SIZE > len(channels):
                break
            block_lsb = [
                channels[block_start + i] & 1 for i in range(_BLOCK_SIZE)
            ]
            syndrome = _syndrome(block_lsb)
            out.extend(_int_to_bits(syndrome, _PAYLOAD_BITS_PER_BLOCK))
            block_index += 1
        return out[:bit_count]


def _syndrome(lsbs: list[int]) -> int:
    """Синдром (4 бита) для 15-битного блока: XOR индексов единичных битов."""
    result = 0
    for index, bit in enumerate(lsbs, start=1):
        if bit:
            result ^= index
    return result


def _bits_to_int(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _int_to_bits(value: int, width: int) -> list[int]:
    return [(value >> (width - 1 - shift)) & 1 for shift in range(width)]


def _xor_int(left: int, right: int) -> int:
    return left ^ right
