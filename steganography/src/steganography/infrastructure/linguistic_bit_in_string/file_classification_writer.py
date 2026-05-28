"""Запись результатов классификации в текстовый файл.

Формат строки: ``<ответ>\\t<гласных>\\t<строка>`` — удобен для дальнейшей
обработки и одновременно человекочитаем.
"""

from pathlib import Path

from steganography.domain.linguistic_bit_in_string.ports.classification_writer import (
    ClassificationWriter,
)
from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)


class FileClassificationWriter(ClassificationWriter):
    """Реализация порта записи в обычный UTF-8-файл."""

    def write(
        self, classifications: list[StringClassification], path: Path,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"{item.answer}\t{item.feature_value}\t{item.text}"
            for item in classifications
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
