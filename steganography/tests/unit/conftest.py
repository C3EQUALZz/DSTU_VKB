"""Общие фикстуры для unit-тестов."""

import pytest

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


@pytest.fixture
def encoding_registry() -> EncodingRegistry:
    return EncodingRegistry()


@pytest.fixture
def russian_language() -> RussianLanguageStatistics:
    return RussianLanguageStatistics()


@pytest.fixture
def formatting_detector() -> FormattingDetector:
    return FormattingDetector()


@pytest.fixture
def code_decoder(
    encoding_registry: EncodingRegistry,
    russian_language: RussianLanguageStatistics,
) -> CodeDecoder:
    return CodeDecoder(
        registry=encoding_registry,
        language=russian_language,
        min_score=0.8,
    )
