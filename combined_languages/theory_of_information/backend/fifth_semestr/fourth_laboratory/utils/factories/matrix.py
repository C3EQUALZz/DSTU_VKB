from typing import List, Literal

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
    GMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
    HMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    Factory


class MatrixFactory(Factory):
    @classmethod
    def create(cls, matrix: List[List[int]], matrix_type: Literal["G", "H"]) -> Matrix:
        if matrix_type in ("G", "generator", "порождающая"):
            return GMatrix(matrix)
        if matrix_type in ("H", "checks", "проверочная"):
            return HMatrix(matrix)
        raise ValueError("Неправильный тип матрицы. У вас на выбор есть 'G' или 'H'.")
