"""ExtractLsbBmpCommand + Handler: извлечь сообщение из BMP-контейнера."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.lsb_bmp_vigenere import (
    ExtractLsbBmpView,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.lsb_bmp_vigenere.services.secret_extractor import (
    SecretExtractor,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExtractLsbBmpCommand:
    """Прочитать BMP, извлечь сообщение по известному ключу."""

    container_path: Path
    key: str


@final
class ExtractLsbBmpCommandHandler:
    """Координирует чтение BMP и извлечение сообщения."""

    def __init__(
        self,
        reader: BmpReader,
        extractor: SecretExtractor,
    ) -> None:
        self._reader: Final[BmpReader] = reader
        self._extractor: Final[SecretExtractor] = extractor

    async def __call__(self, data: ExtractLsbBmpCommand) -> ExtractLsbBmpView:
        logger.info("LSB+Виженер: извлечение из %s", data.container_path)
        image = self._reader.read(data.container_path)
        plaintext = self._extractor.extract(image, data.key)
        logger.info(
            "LSB+Виженер: восстановлено %d символов сообщения", len(plaintext),
        )
        return ExtractLsbBmpView(
            input_image=data.container_path,
            plaintext=plaintext,
            ciphertext_bytes=len(plaintext.encode("utf-8")),
        )
