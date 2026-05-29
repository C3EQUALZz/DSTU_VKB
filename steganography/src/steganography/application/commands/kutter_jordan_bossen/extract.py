"""ExtractKjbCommand + Handler: извлечение сообщения методом КДБ."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.kutter_jordan_bossen import (
    ExtractKjbView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.kutter_jordan_bossen.services.kjb_extractor import (
    KjbExtractor,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_parameters import (
    KjbParameters,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)

_LENGTH_PREFIX_BITS: Final[int] = 32


@dataclass(frozen=True, slots=True)
class ExtractKjbCommand:
    """Параметры извлечения сообщения методом КДБ."""

    container_path: Path
    lambda_factor: float
    seed: int


@final
class ExtractKjbCommandHandler:
    """Прочитать 32-битную длину, затем нужное число байт сообщения."""

    def __init__(
        self,
        reader: BmpReader,
        extractor: KjbExtractor,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._extractor: Final[KjbExtractor] = extractor

    async def __call__(self, data: ExtractKjbCommand) -> ExtractKjbView:
        image = self._reader.read(data.container_path)
        params = KjbParameters(
            lambda_factor=data.lambda_factor,
            seed=data.seed,
        )
        length_bits = self._extractor.extract(
            image, _LENGTH_PREFIX_BITS, params,
        )
        message_length = _bits_to_int(length_bits)
        total_bits = _LENGTH_PREFIX_BITS + message_length * 8
        full_bits = self._extractor.extract(image, total_bits, params)
        message_bits = full_bits[_LENGTH_PREFIX_BITS:]
        message = _bits_to_bytes(message_bits).decode("utf-8", errors="replace")
        logger.info("КДБ: извлечено %d байт сообщения", message_length)
        return ExtractKjbView(
            input_image=data.container_path,
            message=message,
            lambda_factor=data.lambda_factor,
            seed=data.seed,
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
