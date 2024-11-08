from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
    GMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
    HMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    Factory


class MatrixFactory(Factory):
    @staticmethod
    def create(matrix: list[list[int]], matrix_type: str) -> Matrix:
        if matrix_type in ("G", "generator", "порождающая"):
            return GMatrix(matrix)
        if matrix_type in ("H", "checks", "проверочная"):
            return HMatrix(matrix)
        raise ValueError("Invalid matrix type. Use 'G' or 'H'.")
