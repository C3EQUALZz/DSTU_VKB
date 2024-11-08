from typing import List

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix, \
    SystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories import MatrixFactory


class HMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def to_systematic_form(self) -> "HSystematicMatrix":
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.

        Returns:
            NDArray[np.int_]: Модифицированная проверочная матрица в систематическом виде.
        """
        # Создаем копию матрицы для изменений и определяем размер
        return MatrixFactory.create_systematic_matrix(self, "H")


class HSystematicMatrix(SystematicMatrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def find_another_type_matrix(self) -> "SystematicMatrix":
        return MatrixFactory.create_systematic_matrix(self, "H")
