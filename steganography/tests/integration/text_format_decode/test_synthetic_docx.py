"""Интеграционный roundtrip: строим docx через python-docx → читаем → декодируем."""

import asyncio
from pathlib import Path

import pytest

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.infrastructure.text_format_decode.docx_reader import (
    DocxFormattingReaderImpl,
)
from tests.integration.factories.docx_builder import (
    build_docx_with_size_hiding,
    build_uniform_docx,
)

_COVER = "Верба зацвела весной апрель верба верба весна апрель зацвела. " * 6


@pytest.mark.parametrize(
    ("codec", "expected_encoding", "secret"),
    [
        ("windows-1251", "Windows-1251", "Один бог забыл - другой поможет."),
        ("cp866", "cp866", "Ветер дует, но горы не двигаются."),
    ],
)
def test_size_roundtrip(
    detect_handler: DetectSecretCommandHandler,
    tmp_path: Path,
    codec: str,
    expected_encoding: str,
    secret: str,
) -> None:
    bits = "".join(f"{b:08b}" for b in secret.encode(codec))
    cover = _COVER[: max(len(bits) + 16, len(_COVER))]
    docx_path = build_docx_with_size_hiding(
        tmp_path / "synthetic.docx", cover, bits,
    )

    view = asyncio.run(
        detect_handler(DetectSecretCommand(docx_path=docx_path)),
    )

    assert view.success, view.error
    assert view.method is not None
    assert view.method.param is FormattingParam.SIZE
    assert view.encoding is not None
    assert view.encoding.name == expected_encoding
    assert view.message == secret


def test_reader_returns_chars_for_real_document(tmp_path: Path) -> None:
    docx_path = build_uniform_docx(tmp_path / "plain.docx", "привет")

    chars = DocxFormattingReaderImpl().read(docx_path)

    assert "".join(c.char for c in chars) == "привет"


def test_uniform_document_reports_no_signal(
    detect_handler: DetectSecretCommandHandler,
    tmp_path: Path,
) -> None:
    docx_path = build_uniform_docx(
        tmp_path / "uniform.docx", "All chars share the same formatting",
    )

    view = asyncio.run(
        detect_handler(DetectSecretCommand(docx_path=docx_path)),
    )

    assert not view.success
    assert view.error == "метод сокрытия не обнаружен"
