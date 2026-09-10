"""CharFormatting — символ контейнера с предписанным значением параметра."""

from dataclasses import dataclass
from typing import Final

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)

#: Значение-сентинел «вычислить от исходного форматирования run'а».
#: Используется при встраивании в существующий docx без явных --zero/--one:
#: нулевые биты оставляют форматирование нетронутым, единичные получают
#: минимальную дельту от исходного значения (см. DocxContainerWriterImpl).
AUTO_VALUE: Final[str] = "auto"


@dataclass(frozen=True, slots=True)
class CharFormatting:
    """Один символ результата и значение параметра, которое к нему применить."""

    char: str
    param: FormattingParam
    value: str
    is_one: bool
