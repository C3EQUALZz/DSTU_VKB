"""EmbedKjbCommand + Handler: встраивание сообщения методом КДБ."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.kutter_jordan_bossen import (
    EmbedKjbView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.common.bmp.bmp_writer import BmpWriter
from steganography.domain.kutter_jordan_bossen.services.kjb_embedder import (
    KjbEmbedder,
)
from steganography.domain.kutter_jordan_bossen.value_objects.kjb_parameters import (
    KjbParameters,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class EmbedKjbCommand:
    """Параметры встраивания сообщения методом КДБ."""

    cover_path: Path
    output_path: Path
    secret_text: str
    lambda_factor: float
    seed: int


@final
class EmbedKjbCommandHandler:
    """Прочитать BMP, встроить биты сообщения и сохранить новый BMP."""

    def __init__(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        embedder: KjbEmbedder,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._writer: Final[BmpWriter] = writer
        self._embedder: Final[KjbEmbedder] = embedder

    async def __call__(self, data: EmbedKjbCommand) -> EmbedKjbView:
        cover = self._reader.read(data.cover_path)
        bits = _text_to_bits(data.secret_text)
        params = KjbParameters(
            lambda_factor=data.lambda_factor,
            seed=data.seed,
        )
        logger.info(
            "КДБ: встраивание %d бит в %s (λ=%.3f, seed=%d)",
            len(bits), data.cover_path, data.lambda_factor, data.seed,
        )
        result, stats = self._embedder.embed(cover, bits, params)
        self._writer.write(result, data.output_path)
        logger.info(
            "КДБ: записано в %s, использовано %d пикселей",
            data.output_path, stats.payload_bits,
        )
        return EmbedKjbView(
            input_image=data.cover_path,
            output_image=data.output_path,
            secret_text=data.secret_text,
            payload_bits=stats.payload_bits,
            container_pixels=stats.container_pixels,
            lambda_factor=data.lambda_factor,
            seed=data.seed,
        )


def _text_to_bits(text: str) -> list[int]:
    data = text.encode("utf-8")
    length_bits = [(len(data) >> (31 - shift)) & 1 for shift in range(32)]
    body_bits = [
        (byte >> (7 - shift)) & 1
        for byte in data
        for shift in range(8)
    ]
    return length_bits + body_bits
