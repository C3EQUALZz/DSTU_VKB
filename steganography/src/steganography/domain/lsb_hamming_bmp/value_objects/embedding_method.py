"""EmbeddingMethod — каким алгоритмом встраивать биты в LSB BMP."""

from enum import Enum


class EmbeddingMethod(str, Enum):
    """Три метода ПР7: простой LSB-R, мягкий LSB-M, эффективный Hamming."""

    LSB_REPLACEMENT = "lsb-r"
    LSB_MATCHING = "lsb-m"
    HAMMING_15_11 = "hamming-15-11"

    @property
    def human_name(self) -> str:
        return _HUMAN[self]


_HUMAN: dict[EmbeddingMethod, str] = {
    EmbeddingMethod.LSB_REPLACEMENT: "LSB-Replacement",
    EmbeddingMethod.LSB_MATCHING: "LSB-Matching",
    EmbeddingMethod.HAMMING_15_11: "Хемминг (15,11)",
}
