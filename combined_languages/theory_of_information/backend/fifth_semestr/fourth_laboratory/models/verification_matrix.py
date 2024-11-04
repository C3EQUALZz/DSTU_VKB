import numpy as np
import numpy.typing as npt
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
        GSystematicMatrix


class HMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def to_systematic_form(self) -> npt.NDArray[np.int_]:
        """
        Находит систематический вид матрицы, удаляя столбцы с единственным значением 1.

        Returns:
            NDArray[np.int_]: Модифицированная проверочная матрица в систематическом виде.
        """
        # Создаем копию матрицы для изменений и определяем размер
        rows, cols = self.matrix.shape

        # Удаление столбцов с единственной единицей
        columns_to_delete = [i for i in range(cols) if np.sum(self.matrix[:, i] == 1) == 1]
        matrix_reduced = np.delete(self.matrix, columns_to_delete, axis=1)

        # Создание единичной матрицы размера (rows, rows)
        identity_matrix = np.eye(rows, dtype=int)

        return HSystematicMatrix(np.hstack((matrix_reduced, identity_matrix)).tolist())


class HSystematicMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def find_generator_matrix(self) -> "GSystematicMatrix":
        return np.hstack((np.eye(self.matrix.shape[1] - self.matrix.shape[0]), self.matrix.transpose()))
