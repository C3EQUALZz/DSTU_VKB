"""SecretPayload — что и как встраивать в контейнер."""

from dataclasses import dataclass

from steganography.domain.common.encodings.encoding import Encoding
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)


@dataclass(frozen=True, slots=True)
class SecretPayload:
    """Секретный текст + кодировка + метод форматирования для встраивания."""

    secret_text: str
    encoding: Encoding
    method: FormattingMethod
