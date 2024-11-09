from typing import List, Literal, TYPE_CHECKING

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
    GMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
    HMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    Factory

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix


class MatrixFactory(Factory):
    @classmethod
    def create(cls, matrix: List[List[int]], matrix_type: Literal["G", "H"]) -> "Matrix":
        if matrix_type in ("G", "generator", "порождающая"):
            return GMatrix(matrix)
        if matrix_type in ("H", "checks", "проверочная"):
            return HMatrix(matrix)
        raise ValueError(f"Неправильный тип матрицы {matrix_type}. У вас на выбор есть 'G' или 'H'.")
