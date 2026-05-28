"""ClassifyStringsCommand + Handler: классификация строк из входного файла."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from steganography.application.common.views.linguistic_bit_in_string import (
    ClassifyStringsView,
)
from steganography.domain.linguistic_bit_in_string.ports.classification_writer import (
    ClassificationWriter,
)
from steganography.domain.linguistic_bit_in_string.ports.string_reader import (
    StringReader,
)
from steganography.domain.linguistic_bit_in_string.services.parity_classifier import (
    ParityClassifier,
)
from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ClassifyStringsCommand:
    """Запрос: прочитать строки из ``input_path``, классифицировать, записать."""

    input_path: Path
    output_path: Path


@final
class ClassifyStringsCommandHandler:
    """Прогоняет файл строк через ``ParityClassifier`` и сохраняет результат."""

    def __init__(
        self,
        reader: StringReader,
        classifier: ParityClassifier,
        writer: ClassificationWriter,
    ) -> None:
        self._reader: Final[StringReader] = reader
        self._classifier: Final[ParityClassifier] = classifier
        self._writer: Final[ClassificationWriter] = writer

    async def __call__(
        self, data: ClassifyStringsCommand,
    ) -> ClassifyStringsView:
        logger.info("Лингв. ПР3: чтение строк из %s", data.input_path)
        strings = self._reader.read(data.input_path)
        logger.info("Лингв. ПР3: прочитано строк: %d", len(strings))

        classifications: list[StringClassification] = [
            self._classifier.classify(text) for text in strings
        ]
        yes_count = sum(1 for c in classifications if c.bit == 1)
        no_count = len(classifications) - yes_count

        self._writer.write(classifications, data.output_path)
        logger.info(
            "Лингв. ПР3: записано %d результатов в %s "
            "(ДА: %d, НЕТ: %d)",
            len(classifications), data.output_path, yes_count, no_count,
        )
        return ClassifyStringsView(
            input_path=data.input_path,
            output_path=data.output_path,
            classifications=classifications,
            yes_count=yes_count,
            no_count=no_count,
        )
