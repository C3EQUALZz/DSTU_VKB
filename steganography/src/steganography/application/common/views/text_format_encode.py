"""Views для презентации результатов работы «Энкод docx»."""

from dataclasses import dataclass
from pathlib import Path

from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)


@dataclass(frozen=True, slots=True)
class EncodeSecretView:
    """Результат встраивания сообщения в контейнер."""

    output_path: Path
    success: bool
    secret_text: str
    encoding_name: str
    method: FormattingMethod | None
    payload_bits: int
    container_chars: int
    error: str | None = None
