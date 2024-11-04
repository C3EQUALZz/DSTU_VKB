from typing import TYPE_CHECKING, List

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
        HSystematicMatrix


class GMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def to_systematic_form(self) -> "GSystematicMatrix":
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

        return GSystematicMatrix(np.hstack((identity_matrix, matrix_reduced)).tolist())


class GSystematicMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def find_verification_matrix(self) -> "HSystematicMatrix":
        n = self.matrix.shape[1]
        k = self.matrix.shape[0]
        return np.hstack((self.matrix.transpose(), np.eye(n - k)))
