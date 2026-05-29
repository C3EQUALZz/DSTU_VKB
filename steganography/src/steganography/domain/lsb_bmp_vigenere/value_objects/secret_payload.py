"""SecretPayload — текст сообщения и ключ Виженера для встраивания."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecretPayload:
    """Что встраивать в BMP: открытый текст и ключ для шифра Виженера."""

    plaintext: str
    key: str
