"""Фабрики тестовых контейнеров из размеченных символов."""

from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


def container_from_bits(
    bits: str,
    *,
    param: FormattingParam = FormattingParam.SIZE,
    zero_value: str = "28",
    one_value: str = "29",
    cover_text: str | None = None,
) -> list[FormattedChar]:
    """Построить контейнер, где i-й символ кодирует i-й бит через param."""
    cover: str = cover_text or ("a" * len(bits))
    if len(cover) != len(bits):
        msg = "длина cover_text должна совпадать с длиной bits"
        raise ValueError(msg)
    return [
        FormattedChar(
            char=ch,
            attrs={param: one_value if b == "1" else zero_value},
        )
        for ch, b in zip(cover, bits, strict=True)
    ]


def container_from_text(
    text: str,
    codec: str,
    *,
    param: FormattingParam = FormattingParam.SIZE,
    zero_value: str = "28",
    one_value: str = "29",
    trailing_zero_bits: int = 16,
) -> list[FormattedChar]:
    """Закодировать текст в биты (8 бит/символ) и собрать контейнер."""
    data: bytes = text.encode(codec)
    bits: str = "".join(f"{b:08b}" for b in data) + "0" * trailing_zero_bits
    return container_from_bits(
        bits,
        param=param,
        zero_value=zero_value,
        one_value=one_value,
    )


def uniform_container(
    length: int,
    *,
    param: FormattingParam = FormattingParam.SIZE,
    value: str = "28",
) -> list[FormattedChar]:
    """Контейнер без сокрытия — все символы с одинаковым форматированием."""
    return [
        FormattedChar(char="a", attrs={param: value}) for _ in range(length)
    ]
