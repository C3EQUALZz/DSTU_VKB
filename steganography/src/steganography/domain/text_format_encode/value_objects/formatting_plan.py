"""FormattingPlan — полный план форматирования контейнера-результата."""

from dataclasses import dataclass, field

from steganography.domain.text_format_encode.value_objects.char_formatting import (
    CharFormatting,
)


@dataclass(frozen=True, slots=True)
class FormattingPlan:
    """План форматирования символов + разметка строк и базовый шрифт.

    :attr:`line_lengths` задаёт, по сколько символов из :attr:`chars`
    ложится в каждую строку контейнера-результата — так писатель
    воссоздаёт исходное разбиение на абзацы/строки.
    """

    chars: tuple[CharFormatting, ...]
    payload_bits: int
    line_lengths: tuple[int, ...] = field(default_factory=tuple)
    font_name: str | None = None
    font_size: str | None = None
