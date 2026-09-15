"""Интеграционный roundtrip: встраиваем через реальный writer, декодируем обратно."""

import asyncio
from pathlib import Path

import pytest
from docx import Document

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.application.commands.text_format_encode.encode import (
    EncodeSecretCommand,
    EncodeSecretCommandHandler,
)
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
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
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)
from steganography.infrastructure.text_format_decode.docx_reader import (
    DocxFormattingReaderImpl,
)
from steganography.infrastructure.text_format_encode.docx_container_writer import (
    DocxContainerWriterImpl,
)
from steganography.infrastructure.text_format_encode.docx_cover_text_reader import (
    DocxCoverTextReaderImpl,
)
from steganography.domain.text_format_encode.value_objects.char_formatting import AUTO_VALUE

_COVER = "Верба зацвела весной апрель верба верба весна апрель зацвела. " * 8


@pytest.mark.parametrize("param", [
    FormattingParam.SIZE, FormattingParam.COLOR,
    FormattingParam.SCALE, FormattingParam.SPACING,
])
def test_relative_formatting_roundtrip(tmp_path: Path, param: FormattingParam) -> None:
    source = tmp_path / "cover.docx"
    output = tmp_path / "encoded.docx"
    document = Document()
    document.add_paragraph(_COVER)
    document.save(source)
    result = asyncio.run(_encode_handler()(EncodeSecretCommand(
        secret_text="Ветер дует.",
        cover=DocxCoverTextReaderImpl().read(source),
        encoding_name="Windows-1251", param=param,
        zero_value=AUTO_VALUE, one_value=AUTO_VALUE, output_path=output,
    )))
    assert result.success, result.error
    decoded = asyncio.run(_decode_handler()(DetectSecretCommand(docx_path=output)))
    assert decoded.success, decoded.error
    assert decoded.message == "Ветер дует."
    assert decoded.method is not None
    assert decoded.method.param is param


def _encode_handler() -> EncodeSecretCommandHandler:
    return EncodeSecretCommandHandler(
        registry=EncodingRegistry(),
        plan_builder=ContainerPlanBuilder(),
        writer=DocxContainerWriterImpl(),
    )


def _decode_handler() -> DetectSecretCommandHandler:
    return DetectSecretCommandHandler(
        reader=DocxFormattingReaderImpl(),
        detector=FormattingDetector(),
        decoder=CodeDecoder(
            registry=EncodingRegistry(),
            language=RussianLanguageStatistics(),
            min_score=0.8,
        ),
    )


@pytest.mark.parametrize(
    ("encoding_name", "param", "secret"),
    [
        ("Windows-1251", FormattingParam.SIZE, "Один бог забыл."),
        ("cp866", FormattingParam.COLOR, "Ветер дует."),
        ("КОИ-8R", FormattingParam.SCALE, "Нет врага опаснее дурака."),
        ("Windows-1251", FormattingParam.SPACING, "Дела громче слов."),
    ],
)
def test_encode_then_decode_recovers_secret(
    tmp_path: Path,
    encoding_name: str,
    param: FormattingParam,
    secret: str,
) -> None:
    defaults = {
        FormattingParam.SIZE: ("28", "29"),
        FormattingParam.COLOR: ("000000", "010000"),
        FormattingParam.SCALE: ("100", "99"),
        FormattingParam.SPACING: ("0", "2"),
    }
    zero_value, one_value = defaults[param]
    output = tmp_path / "encoded.docx"

    encode_view = asyncio.run(
        _encode_handler()(
            EncodeSecretCommand(
                secret_text=secret,
                cover=CoverText.from_plain(_COVER),
                encoding_name=encoding_name,
                param=param,
                zero_value=zero_value,
                one_value=one_value,
                output_path=output,
            ),
        ),
    )
    assert encode_view.success, encode_view.error

    decode_view = asyncio.run(
        _decode_handler()(DetectSecretCommand(docx_path=output)),
    )
    assert decode_view.success, decode_view.error
    assert decode_view.message == secret
    assert decode_view.method is not None
    assert decode_view.method.param is param
    assert decode_view.encoding is not None
    assert decode_view.encoding.name == encoding_name
