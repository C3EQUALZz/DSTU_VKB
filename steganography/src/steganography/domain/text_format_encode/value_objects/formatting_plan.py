"""FormattingPlan — полный план форматирования контейнера-результата."""

from dataclasses import dataclass

from steganography.domain.text_format_encode.value_objects.char_formatting import (
    CharFormatting,
)


@dataclass(frozen=True, slots=True)
class FormattingPlan:
    """Последовательность форматирований символов + длина полезных бит."""

    chars: tuple[CharFormatting, ...]
    payload_bits: int
