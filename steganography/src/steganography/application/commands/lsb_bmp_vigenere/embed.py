"""EmbedLsbBmpCommand + Handler: встроить сообщение в BMP-контейнер."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.lsb_bmp_vigenere import (
    EmbedLsbBmpView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.common.bmp.bmp_writer import BmpWriter
from steganography.domain.lsb_bmp_vigenere.services.secret_embedder import (
    SecretEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.value_objects.secret_payload import (
    SecretPayload,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class EmbedLsbBmpCommand:
    """Прочитать BMP, встроить сообщение и сохранить новый BMP."""

    cover_path: Path
    output_path: Path
    secret_text: str
    key: str


@final
class EmbedLsbBmpCommandHandler:
    """Координирует чтение BMP, шифр + LSB-встраивание и запись результата."""

    def __init__(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        embedder: SecretEmbedder,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._writer: Final[BmpWriter] = writer
        self._embedder: Final[SecretEmbedder] = embedder

    async def __call__(self, data: EmbedLsbBmpCommand) -> EmbedLsbBmpView:
        logger.info("LSB+Виженер: чтение контейнера %s", data.cover_path)
        cover = self._reader.read(data.cover_path)
        payload = SecretPayload(plaintext=data.secret_text, key=data.key)

        result = self._embedder.embed(cover, payload)
        self._writer.write(result, data.output_path)

        plaintext_bytes = len(data.secret_text.encode("utf-8"))
        # +14 — две 7-байтные метки start_marker/end_marker, как в MarkerPackager
        ciphertext_bytes = plaintext_bytes + 14
        payload_bits = ciphertext_bytes * 8
        capacity_bits = cover.total_pixels * 3

        logger.info(
            "LSB+Виженер: записано %d бит из %d возможных в %s",
            payload_bits, capacity_bits, data.output_path,
        )
        return EmbedLsbBmpView(
            input_image=data.cover_path,
            output_image=data.output_path,
            plaintext_bytes=plaintext_bytes,
            ciphertext_bytes=ciphertext_bytes - 14,
            payload_bits=payload_bits,
            capacity_bits=capacity_bits,
        )
