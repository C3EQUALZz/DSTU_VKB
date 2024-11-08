from typing import List, cast

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_systematic_matrix import \
    HSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.systematic import \
    SystematicMatrixFactory


class HMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)
        SystematicMatrixFactory.register("H", HSystematicMatrix)

    def to_systematic_form(self) -> "HSystematicMatrix":
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.

        Returns:
            NDArray[np.int_]: Модифицированная проверочная матрица в систематическом виде.
        """
        return cast(HSystematicMatrix, SystematicMatrixFactory.create(self, "H"))
