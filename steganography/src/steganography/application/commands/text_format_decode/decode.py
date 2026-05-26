"""DetectSecretCommand + CommandHandler: декодирование одного docx-контейнера."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.text_format_decode import (
    DetectSecretView,
)
from steganography.domain.text_format_decode.ports.docx_formatting_reader import (
    DocxFormattingReader,
)
from steganography.domain.text_format_decode.services.code_decoder import (
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DetectSecretCommand:
    """Найти скрытое сообщение в одном docx-файле."""

    docx_path: Path


@final
class DetectSecretCommandHandler:
    """Координирует чтение docx, детекцию метода и декодирование сообщения."""

    def __init__(
        self,
        reader: DocxFormattingReader,
        detector: FormattingDetector,
        decoder: CodeDecoder,
    ) -> None:
        self._reader: Final[DocxFormattingReader] = reader
        self._detector: Final[FormattingDetector] = detector
        self._decoder: Final[CodeDecoder] = decoder

    async def __call__(self, data: DetectSecretCommand) -> DetectSecretView:
        logger.info("Декод docx: чтение контейнера %s", data.docx_path)
        chars = self._reader.read(data.docx_path)
        logger.info("Декод docx: прочитано символов: %d", len(chars))

        method = self._detector.detect(chars)
        if method is None:
            logger.warning("Декод docx: метод сокрытия не обнаружен")
            return DetectSecretView(
                docx_path=data.docx_path,
                success=False,
                method=None,
                encoding=None,
                bit_sequence="",
                message="",
                error="метод сокрытия не обнаружен",
            )
        logger.info(
            "Декод docx: метод %s — для 0 «%s», для 1 «%s»",
            method.param.value, method.zero_value, method.one_value,
        )

        decoded = self._decoder.decode(chars, method)
        if decoded is None:
            logger.warning("Декод docx: ни одна кодировка не дала осмысленный текст")
            return DetectSecretView(
                docx_path=data.docx_path,
                success=False,
                method=method,
                encoding=None,
                bit_sequence="",
                message="",
                error="ни одна кодировка не дала осмысленный текст",
            )
        logger.info(
            "Декод docx: найдено сообщение в кодировке %s, длина %d",
            decoded.encoding.name, len(decoded.message),
        )
        return DetectSecretView(
            docx_path=data.docx_path,
            success=True,
            method=decoded.method,
            encoding=decoded.encoding,
            bit_sequence=decoded.bit_sequence,
            message=decoded.message,
        )
