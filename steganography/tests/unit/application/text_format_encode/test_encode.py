"""Тесты application-handler'а EncodeSecretCommandHandler через fake-writer."""

import asyncio
from pathlib import Path

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
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)
from tests.unit.factories.fake_container_writer import FakeContainerWriter

_OUTPUT = Path("/in-memory/out.docx")


def _make_handler(writer: FakeContainerWriter) -> EncodeSecretCommandHandler:
    return EncodeSecretCommandHandler(
        registry=EncodingRegistry(),
        plan_builder=ContainerPlanBuilder(),
        writer=writer,
    )


def test_handler_writes_plan_and_returns_success() -> None:
    writer = FakeContainerWriter()
    handler = _make_handler(writer)
    command = EncodeSecretCommand(
        secret_text="Без труда не вытащишь и рыбку из пруда.",
        cover=CoverText.from_plain("a" * 2000),
        encoding_name="cp866",
        param=FormattingParam.SIZE,
        zero_value="28",
        one_value="29",
        output_path=_OUTPUT,
    )

    view = asyncio.run(handler(command))

    assert view.success
    assert view.payload_bits > 0
    assert writer.last_plan is not None
    assert writer.last_path == _OUTPUT
    assert writer.last_plan.payload_bits == view.payload_bits


def test_handler_reports_unknown_encoding() -> None:
    writer = FakeContainerWriter()
    handler = _make_handler(writer)
    command = EncodeSecretCommand(
        secret_text="привет",
        cover=CoverText.from_plain("a" * 100),
        encoding_name="UTF-8000",
        param=FormattingParam.SIZE,
        zero_value="28",
        one_value="29",
        output_path=_OUTPUT,
    )

    view = asyncio.run(handler(command))

    assert not view.success
    assert view.error == "неизвестная кодировка"
    assert writer.last_plan is None


def test_handler_reports_container_too_small() -> None:
    writer = FakeContainerWriter()
    handler = _make_handler(writer)
    command = EncodeSecretCommand(
        secret_text="очень длинное секретное сообщение",
        cover=CoverText.from_plain("мало"),
        encoding_name="Windows-1251",
        param=FormattingParam.SIZE,
        zero_value="28",
        one_value="29",
        output_path=_OUTPUT,
    )

    view = asyncio.run(handler(command))

    assert not view.success
    assert view.error is not None
    assert writer.last_plan is None
