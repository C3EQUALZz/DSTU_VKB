from typing import TYPE_CHECKING

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    Factory

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import \
        SystematicMatrix


class SystematicMatrixFactory(Factory):
    _registry = {}

    @classmethod
    def register(cls, matrix_type: str, matrix_cls) -> None:
        cls._registry[matrix_type] = matrix_cls

    @classmethod
    def create(cls, matrix: "Matrix", matrix_type: str) -> "SystematicMatrix":
        """
        Создает систематическую матрицу на основе типа.
        """
        matrix_cls = cls._registry[matrix_type]

        rows, cols = matrix.matrix.shape
        columns_to_delete = [i for i in range(cols) if np.sum(matrix.matrix[:, i] == 1) == 1]
        matrix_reduced = np.delete(matrix.matrix, columns_to_delete, axis=1)
        identity_matrix = np.eye(rows, dtype=int)

        if matrix_type in ("G", "generator", "порождающая"):
            return matrix_cls(np.hstack((identity_matrix, matrix_reduced)).tolist())
        if matrix_type in ("H", "checks", "проверочная"):
            return matrix_cls(np.hstack((matrix_reduced, identity_matrix)).tolist())
        raise ValueError("Invalid matrix type. Use 'G' or 'H'.")
