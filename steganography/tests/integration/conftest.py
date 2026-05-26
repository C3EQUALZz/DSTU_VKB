"""Фикстуры интеграционных тестов: реальная инфраструктура и данные."""

from pathlib import Path

import pytest

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommandHandler,
)
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.text_format_decode.language.russian_language_statistics import (
    RussianLanguageStatistics,
)
from steganography.domain.text_format_decode.services.code_decoder import (
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)
from steganography.infrastructure.text_format_decode.docx_reader import (
    DocxFormattingReaderImpl,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_VARIANTS_DIR = (
    _PROJECT_ROOT / "resources" / "steganographic_concealment" / "variants"
)


@pytest.fixture
def variants_dir() -> Path:
    return _VARIANTS_DIR


@pytest.fixture
def detect_handler() -> DetectSecretCommandHandler:
    return DetectSecretCommandHandler(
        reader=DocxFormattingReaderImpl(),
        detector=FormattingDetector(),
        decoder=CodeDecoder(
            registry=EncodingRegistry(),
            language=RussianLanguageStatistics(),
            min_score=0.8,
        ),
    )
