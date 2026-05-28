"""Views для презентации результатов работы «Лингвистическая стег. 1 бит»."""

from dataclasses import dataclass
from pathlib import Path

from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)


@dataclass(frozen=True, slots=True)
class ClassifyStringsView:
    """Сводка по пакетной классификации строк из файла."""

    input_path: Path
    output_path: Path
    classifications: list[StringClassification]
    yes_count: int
    no_count: int
