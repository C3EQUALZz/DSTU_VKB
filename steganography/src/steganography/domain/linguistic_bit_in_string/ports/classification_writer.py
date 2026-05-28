"""Порт записи результатов классификации в выходной файл."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)


@runtime_checkable
class ClassificationWriter(Protocol):
    """Сохраняет результаты классификации в файл."""

    def write(
        self, classifications: list[StringClassification], path: Path,
    ) -> None:
        ...
