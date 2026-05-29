"""EmbedLsbHammingCommand + Handler: встраивание одним из методов ПР7."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.lsb_hamming_bmp import (
    EmbedLsbHammingView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.common.bmp.bmp_writer import BmpWriter
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


@dataclass(frozen=True, slots=True)
class EmbedLsbHammingCommand:
    """Параметры встраивания текстового сообщения в BMP."""

    cover_path: Path
    output_path: Path
    secret_text: str
    method: EmbeddingMethod
    step: int


@final
class EmbedLsbHammingCommandHandler:
    """Выбирает реализацию по методу и записывает результат в файл."""

    def __init__(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        lsb_r: LsbReplacementMethod,
        lsb_m: LsbMatchingMethod,
        hamming: Hamming15_11Method,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._writer: Final[BmpWriter] = writer
        self._lsb_r: Final[LsbReplacementMethod] = lsb_r
        self._lsb_m: Final[LsbMatchingMethod] = lsb_m
        self._hamming: Final[Hamming15_11Method] = hamming

    async def __call__(
        self, data: EmbedLsbHammingCommand,
    ) -> EmbedLsbHammingView:
        cover = self._reader.read(data.cover_path)
        message_bits = _text_to_bits(data.secret_text)
        logger.info(
            "%s: %d бит сообщения в %s (шаг %d)",
            data.method.human_name, len(message_bits), data.cover_path, data.step,
        )

        if data.method is EmbeddingMethod.HAMMING_15_11:
            result, stats = self._hamming.embed(cover, message_bits)
        elif data.method is EmbeddingMethod.LSB_MATCHING:
            result, stats = self._lsb_m.embed(cover, message_bits, data.step)
        else:
            result, stats = self._lsb_r.embed(cover, message_bits, data.step)

        self._writer.write(result, data.output_path)
        logger.info(
            "%s: записано в %s, искажено %d/%d каналов",
            data.method.human_name, data.output_path,
            stats.changed_channels, stats.capacity_bits,
        )
        return EmbedLsbHammingView(
            input_image=data.cover_path,
            output_image=data.output_path,
            method=data.method,
            stats=stats,
        )


def _text_to_bits(text: str) -> list[int]:
    data = text.encode("utf-8")
    # 4-байтовый префикс длины + полезные байты
    length_bits = [
        (len(data) >> (31 - shift)) & 1 for shift in range(32)
    ]
    body_bits = [
        (byte >> (7 - shift)) & 1
        for byte in data
        for shift in range(8)
    ]
    return length_bits + body_bits
