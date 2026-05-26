"""DecodedMessage — успешно расшифрованное сообщение."""

from dataclasses import dataclass

from steganography.domain.common.encodings.encoding import Encoding
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)


@dataclass(frozen=True)
class DecodedMessage:
    """Результат работы декодера для одного контейнера."""

    method: FormattingMethod
    encoding: Encoding
    bit_sequence: str
    message: str
