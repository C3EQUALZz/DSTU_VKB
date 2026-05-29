"""Views для презентации результатов ПР7."""

from dataclasses import dataclass
from pathlib import Path

from steganography.domain.lsb_hamming_bmp.value_objects.embedding_method import (
    EmbeddingMethod,
)
from steganography.domain.lsb_hamming_bmp.value_objects.embedding_stats import (
    EmbeddingStats,
)


@dataclass(frozen=True, slots=True)
class EmbedLsbHammingView:
    """Итог встраивания одним из методов ПР7."""

    input_image: Path
    output_image: Path
    method: EmbeddingMethod
    stats: EmbeddingStats


@dataclass(frozen=True, slots=True)
class ExtractLsbHammingView:
    """Итог извлечения сообщения по выбранному методу."""

    input_image: Path
    method: EmbeddingMethod
    message: str
