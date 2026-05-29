"""Views для презентации результатов ПР6 «LSB в BMP с шифрованием Виженера»."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class EmbedLsbBmpView:
    """Результат встраивания сообщения в BMP-контейнер."""

    input_image: Path
    output_image: Path
    plaintext_bytes: int
    ciphertext_bytes: int
    payload_bits: int
    capacity_bits: int


@dataclass(frozen=True, slots=True)
class ExtractLsbBmpView:
    """Результат извлечения сообщения из BMP-контейнера."""

    input_image: Path
    plaintext: str
    ciphertext_bytes: int
