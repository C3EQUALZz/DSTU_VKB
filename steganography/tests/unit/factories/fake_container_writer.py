"""In-memory реализация порта записи контейнера для unit-тестов."""

from pathlib import Path
from typing import final

from steganography.domain.text_format_encode.ports.container_writer import (
    ContainerWriter,
)
from steganography.domain.text_format_encode.value_objects.formatting_plan import (
    FormattingPlan,
)


@final
class FakeContainerWriter(ContainerWriter):
    """Запоминает последний записанный план, не трогая файловую систему."""

    def __init__(self) -> None:
        self.last_plan: FormattingPlan | None = None
        self.last_path: Path | None = None

    def write(self, plan: FormattingPlan, path: Path) -> None:
        self.last_plan = plan
        self.last_path = path
