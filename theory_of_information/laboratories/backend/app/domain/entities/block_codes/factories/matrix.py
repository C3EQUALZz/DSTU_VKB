from typing import TYPE_CHECKING, List, Literal

from app.domain.entities.block_codes.factories.base import Factory
from app.domain.entities.block_codes.generator_matrix import GMatrix
from app.domain.entities.block_codes.verification_matrix import HMatrix

if TYPE_CHECKING:
    from app.domain.entities.block_codes.base import Matrix


class MatrixFactory(Factory):
    @classmethod
    def create(
        cls, matrix: List[List[int]], matrix_type: Literal["G", "H"]
    ) -> "Matrix":
        if matrix_type in ("G", "generator", "порождающая"):
            return GMatrix(matrix)
        if matrix_type in ("H", "checks", "проверочная"):
            return HMatrix(matrix)
        raise ValueError(
            f"Неправильный тип матрицы {matrix_type}. У вас на выбор есть 'G' или 'H'."
        )
