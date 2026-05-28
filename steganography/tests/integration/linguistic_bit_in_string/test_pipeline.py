"""Интеграционный тест: реальный файл → handler → реальный файл."""

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
from steganography.infrastructure.linguistic_bit_in_string.file_classification_writer import (
    FileClassificationWriter,
)
from steganography.infrastructure.linguistic_bit_in_string.file_string_reader import (
    FileStringReader,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SAMPLES = _PROJECT_ROOT.parent / "resources" / "linguistic_samples"


def _make_handler() -> ClassifyStringsCommandHandler:
    return ClassifyStringsCommandHandler(
        reader=FileStringReader(),
        classifier=ParityClassifier(vowel_counter=VowelCounter()),
        writer=FileClassificationWriter(),
    )


def test_sample_file_has_ten_yes_and_ten_no(tmp_path: Path) -> None:
    output = tmp_path / "out.txt"
    view = asyncio.run(
        _make_handler()(
            ClassifyStringsCommand(
                input_path=_SAMPLES / "input.txt",
                output_path=output,
            ),
        ),
    )
    assert view.yes_count == 10
    assert view.no_count == 10
    assert output.exists()
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 20
    for line in lines:
        answer, _, _ = line.partition("\t")
        assert answer in {"ДА", "НЕТ"}


def test_writer_creates_parents(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "deep" / "out.txt"
    asyncio.run(
        _make_handler()(
            ClassifyStringsCommand(
                input_path=_SAMPLES / "input.txt",
                output_path=output,
            ),
        ),
    )
    assert output.exists()
