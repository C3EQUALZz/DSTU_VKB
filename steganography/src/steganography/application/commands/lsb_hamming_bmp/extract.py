"""ExtractLsbHammingCommand + Handler: извлечение сообщения одним из методов ПР7."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.lsb_hamming_bmp import (
    ExtractLsbHammingView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.lsb_hamming_bmp.services.hamming_15_11_method import (
    Hamming15_11Method,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_matching_method import (
    LsbMatchingMethod,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_replacement_method import (
    LsbReplacementMethod,
)
from steganography.domain.lsb_hamming_bmp.value_objects.embedding_method import (
    EmbeddingMethod,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)

_LENGTH_PREFIX_BITS: Final[int] = 32


@dataclass(frozen=True, slots=True)
class ExtractLsbHammingCommand:
    """Параметры извлечения сообщения из BMP-контейнера."""

    container_path: Path
    method: EmbeddingMethod
    step: int


@final
class ExtractLsbHammingCommandHandler:
    """Читает 32-битную длину, затем нужное число байт и декодирует UTF-8."""

    def __init__(
        self,
        reader: BmpReader,
        lsb_r: LsbReplacementMethod,
        lsb_m: LsbMatchingMethod,
        hamming: Hamming15_11Method,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._lsb_r: Final[LsbReplacementMethod] = lsb_r
        self._lsb_m: Final[LsbMatchingMethod] = lsb_m
        self._hamming: Final[Hamming15_11Method] = hamming

    async def __call__(
        self, data: ExtractLsbHammingCommand,
    ) -> ExtractLsbHammingView:
        image = self._reader.read(data.container_path)

        if data.method is EmbeddingMethod.HAMMING_15_11:
            prefix_bits = self._hamming.extract(image, _LENGTH_PREFIX_BITS)
            length = _bits_to_int(prefix_bits)
            full_bits = self._hamming.extract(
                image, _LENGTH_PREFIX_BITS + length * 8,
            )
        elif data.method is EmbeddingMethod.LSB_MATCHING:
            prefix_bits = self._lsb_m.extract(
                image, _LENGTH_PREFIX_BITS, data.step,
            )
            length = _bits_to_int(prefix_bits)
            full_bits = self._lsb_m.extract(
                image, _LENGTH_PREFIX_BITS + length * 8, data.step,
            )
        else:
            prefix_bits = self._lsb_r.extract(
                image, _LENGTH_PREFIX_BITS, data.step,
            )
            length = _bits_to_int(prefix_bits)
            full_bits = self._lsb_r.extract(
                image, _LENGTH_PREFIX_BITS + length * 8, data.step,
            )

        body_bits = full_bits[_LENGTH_PREFIX_BITS:]
        data_bytes = _bits_to_bytes(body_bits)
        message = data_bytes.decode("utf-8", errors="replace")
        logger.info(
            "%s: извлечено %d байт сообщения", data.method.human_name, length,
        )
        return ExtractLsbHammingView(
            input_image=data.container_path,
            method=data.method,
            message=message,
        )


def _bits_to_int(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _bits_to_bytes(bits: list[int]) -> bytes:
    out = bytearray()
    for offset in range(0, len(bits) - len(bits) % 8, 8):
        byte_value = 0
        for shift in range(8):
            byte_value = (byte_value << 1) | bits[offset + shift]
        out.append(byte_value)
    return bytes(out)
