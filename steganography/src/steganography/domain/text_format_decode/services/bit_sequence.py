"""Утилиты работы с битовой строкой контейнера.

Содержит две функции:

* :func:`build_bit_sequence` собирает биты по выбранному методу;
* :func:`trim_trailing_zeros` отбрасывает «хвостовые» нули по границе
  кодового слова, оставляя только полезную часть.
"""

from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)


def build_bit_sequence(
    chars: list[FormattedChar],
    method: FormattingMethod,
) -> str:
    bits: list[str] = []
    for c in chars:
        value: str | None = c.attrs.get(method.param)
        bits.append("1" if value == method.one_value else "0")
    return "".join(bits)


def trim_trailing_zeros(bits: str, group: int = 8) -> str:
    last_one: int = bits.rfind("1")
    if last_one < 0:
        return ""
    end: int = last_one + 1
    pad: int = (group - end % group) % group
    return bits[: end + pad]
