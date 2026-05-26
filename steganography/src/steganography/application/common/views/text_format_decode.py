"""Views для презентации результатов работы «Декод docx»."""

from dataclasses import dataclass
from pathlib import Path

from steganography.domain.common.encodings.encoding import Encoding
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)


@dataclass(frozen=True, slots=True)
class DetectSecretView:
    """Что показать пользователю по результату анализа одного контейнера."""

    docx_path: Path
    success: bool
    method: FormattingMethod | None
    encoding: Encoding | None
    bit_sequence: str
    message: str
    error: str | None = None
