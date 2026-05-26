"""CharFormatting — символ контейнера с предписанным значением параметра."""

from dataclasses import dataclass

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


@dataclass(frozen=True, slots=True)
class CharFormatting:
    """Один символ результата и значение параметра, которое к нему применить."""

    char: str
    param: FormattingParam
    value: str
    is_one: bool
