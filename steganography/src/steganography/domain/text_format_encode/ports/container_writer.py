"""Порт записи контейнера-результата по плану форматирования."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from steganography.domain.text_format_encode.value_objects.formatting_plan import (
    FormattingPlan,
)


@runtime_checkable
class ContainerWriter(Protocol):
    """Сохраняет план форматирования в docx-файл с скрытым сообщением."""

    def write(self, plan: FormattingPlan, path: Path) -> None:
        ...
