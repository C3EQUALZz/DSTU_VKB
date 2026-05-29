"""Views для презентации результатов КДБ8."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class EmbedKjbView:
    """Итог встраивания сообщения по методу Куттера-Джордана-Боссена."""

    input_image: Path
    output_image: Path
    secret_text: str
    payload_bits: int
    container_pixels: int
    lambda_factor: float
    seed: int


@dataclass(frozen=True, slots=True)
class ExtractKjbView:
    """Итог извлечения сообщения из BMP-контейнера КДБ."""

    input_image: Path
    message: str
    lambda_factor: float
    seed: int
