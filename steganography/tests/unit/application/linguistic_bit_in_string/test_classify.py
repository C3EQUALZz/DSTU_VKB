"""Тесты application-handler'а ClassifyStringsCommandHandler через фейки."""

import asyncio
from pathlib import Path

from steganography.application.commands.linguistic_bit_in_string.classify import (
    ClassifyStringsCommand,
    ClassifyStringsCommandHandler,
)
from steganography.domain.linguistic_bit_in_string.services.parity_classifier import (
    ParityClassifier,
)
from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)
from tests.unit.factories.fake_classification_writer import (
    FakeClassificationWriter,
)
from tests.unit.factories.fake_string_reader import FakeStringReader

_INPUT = Path("/in-memory/input.txt")
_OUTPUT = Path("/in-memory/output.txt")


def _make_handler(
    reader: FakeStringReader, writer: FakeClassificationWriter,
) -> ClassifyStringsCommandHandler:
    return ClassifyStringsCommandHandler(
        reader=reader,
        classifier=ParityClassifier(vowel_counter=VowelCounter()),
        writer=writer,
    )


def test_handler_counts_yes_and_no() -> None:
    reader = FakeStringReader(["Мама мыла раму", "Знание сила"])
    writer = FakeClassificationWriter()
    handler = _make_handler(reader, writer)

    view = asyncio.run(
        handler(ClassifyStringsCommand(input_path=_INPUT, output_path=_OUTPUT)),
    )

    assert view.yes_count == 1
    assert view.no_count == 1
    assert [c.answer for c in view.classifications] == ["ДА", "НЕТ"]
    assert writer.last_path == _OUTPUT
    assert writer.last_items is not None
    assert len(writer.last_items) == 2


def test_handler_handles_empty_input() -> None:
    reader = FakeStringReader([])
    writer = FakeClassificationWriter()
    handler = _make_handler(reader, writer)

    view = asyncio.run(
        handler(ClassifyStringsCommand(input_path=_INPUT, output_path=_OUTPUT)),
    )

    assert view.yes_count == 0
    assert view.no_count == 0
    assert view.classifications == []
