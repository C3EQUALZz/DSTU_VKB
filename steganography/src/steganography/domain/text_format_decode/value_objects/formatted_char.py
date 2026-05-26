"""FormattedChar — символ контейнера с привязанным форматированием."""

from dataclasses import dataclass, field

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


@dataclass(frozen=True)
class FormattedChar:
    """Один символ docx-контейнера и его атрибуты форматирования."""

    char: str
    attrs: dict[FormattingParam, str] = field(default_factory=dict)
