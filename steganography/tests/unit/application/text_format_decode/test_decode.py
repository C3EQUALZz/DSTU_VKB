"""Тесты application-handler'а DetectSecretCommandHandler через fake-ридер."""

import asyncio
from pathlib import Path

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.domain.text_format_decode.services.code_decoder import (
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from tests.unit.factories.fake_docx_formatting_reader import (
    FakeDocxFormattingReader,
)
from tests.unit.factories.formatted_char_factory import (
    container_from_text,
    uniform_container,
)

_ANY_PATH = Path("/in-memory/variant.docx")


def test_handler_returns_success_view(
    formatting_detector: FormattingDetector,
    code_decoder: CodeDecoder,
) -> None:
    secret = "Один бог забыл - другой поможет."
    reader = FakeDocxFormattingReader(
        container_from_text(secret, "windows-1251"),
    )
    handler = DetectSecretCommandHandler(
        reader=reader, detector=formatting_detector, decoder=code_decoder,
    )

    view = asyncio.run(handler(DetectSecretCommand(docx_path=_ANY_PATH)))

    assert view.success
    assert view.message == secret
    assert view.method is not None
    assert view.method.param is FormattingParam.SIZE
    assert view.encoding is not None
    assert view.encoding.name == "Windows-1251"


def test_handler_returns_failure_view_when_no_method(
    formatting_detector: FormattingDetector,
    code_decoder: CodeDecoder,
) -> None:
    reader = FakeDocxFormattingReader(uniform_container(40))
    handler = DetectSecretCommandHandler(
        reader=reader, detector=formatting_detector, decoder=code_decoder,
    )

    view = asyncio.run(handler(DetectSecretCommand(docx_path=_ANY_PATH)))

    assert not view.success
    assert view.error == "метод сокрытия не обнаружен"
