"""Тесты декодера сообщения по битовой строке."""

import pytest

from steganography.domain.text_format_decode.services.code_decoder import (
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)
from tests.unit.factories.formatted_char_factory import container_from_text


@pytest.mark.parametrize(
    ("codec", "expected_name", "secret"),
    [
        ("windows-1251", "Windows-1251", "Один бог забыл - другой поможет."),
        ("windows-1251", "Windows-1251", "стеганография защищает информацию"),
        ("cp866", "cp866", "Один бог забыл - другой поможет."),
    ],
)
def test_recovers_message(
    code_decoder: CodeDecoder,
    formatting_detector: FormattingDetector,
    codec: str,
    expected_name: str,
    secret: str,
) -> None:
    chars = container_from_text(secret, codec)
    method = formatting_detector.detect(chars)
    assert method is not None
    decoded = code_decoder.decode(chars, method)
    assert decoded is not None
    assert decoded.message == secret
    assert decoded.encoding.name == expected_name


def test_recovers_message_with_inverted_roles(
    code_decoder: CodeDecoder,
    formatting_detector: FormattingDetector,
) -> None:
    secret = "Один бог забыл - другой поможет."
    chars = container_from_text(
        secret, "windows-1251", zero_value="29", one_value="28",
    )
    method = formatting_detector.detect(chars)
    assert method is not None
    decoded = code_decoder.decode(chars, method)
    assert decoded is not None
    assert decoded.message == secret
