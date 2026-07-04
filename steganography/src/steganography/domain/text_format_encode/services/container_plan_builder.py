"""ContainerPlanBuilder — строит план форматирования контейнера.

Берёт секретную нагрузку и текст-контейнер, кодирует сообщение в биты и
сопоставляет каждому символу контейнера значение параметра форматирования:
для бита «1» — :attr:`FormattingMethod.one_value`, для «0» (и для хвоста
после конца сообщения) — :attr:`FormattingMethod.zero_value`.
"""

from steganography.domain.text_format_encode.errors.encode_errors import (
    ContainerTooSmallError,
    UnencodableSecretError,
)
from steganography.domain.text_format_encode.value_objects.char_formatting import (
    CharFormatting,
)
from steganography.domain.text_format_encode.value_objects.cover_text import (
    CoverText,
)
from steganography.domain.text_format_encode.value_objects.formatting_plan import (
    FormattingPlan,
)
from steganography.domain.text_format_encode.value_objects.secret_payload import (
    SecretPayload,
)


class ContainerPlanBuilder:
    """Доменный сервис построения плана встраивания."""

    def build(self, payload: SecretPayload, cover: CoverText) -> FormattingPlan:
        cover_text = cover.text
        bits = payload.encoding.encode(payload.secret_text)
        if bits is None:
            raise UnencodableSecretError(payload.encoding.name)
        if len(bits) > len(cover_text):
            raise ContainerTooSmallError(
                required_bits=len(bits),
                available_chars=len(cover_text),
            )

        method = payload.method
        chars: list[CharFormatting] = []
        for index, char in enumerate(cover_text):
            is_one = index < len(bits) and bits[index] == "1"
            chars.append(
                CharFormatting(
                    char=char,
                    param=method.param,
                    value=method.one_value if is_one else method.zero_value,
                    is_one=is_one,
                ),
            )
        return FormattingPlan(
            chars=tuple(chars),
            payload_bits=len(bits),
            line_lengths=cover.line_lengths,
            font_name=cover.font_name,
            font_size=cover.font_size,
        )
