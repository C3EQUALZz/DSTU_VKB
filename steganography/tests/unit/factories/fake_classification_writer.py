"""In-memory реализация порта записи классификаций для unit-тестов."""

from pathlib import Path
from typing import final

from steganography.domain.linguistic_bit_in_string.ports.classification_writer import (
    ClassificationWriter,
)
from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)


@final
class FakeClassificationWriter(ClassificationWriter):
    """Запоминает последнюю записанную партию."""

    def __init__(self) -> None:
        self.last_items: list[StringClassification] | None = None
        self.last_path: Path | None = None

    def write(
        self, classifications: list[StringClassification], path: Path,
    ) -> None:
        self.last_items = list(classifications)
        self.last_path = path
