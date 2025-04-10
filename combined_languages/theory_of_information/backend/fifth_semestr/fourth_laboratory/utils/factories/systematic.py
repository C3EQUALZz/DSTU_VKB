from typing import TYPE_CHECKING, Literal

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    RegistryFactory
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import \
    Registry

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import (
        Matrix, SystematicMatrix)


class SystematicMatrixFactory(RegistryFactory):
    @classmethod
    def create(
        cls, matrix: "Matrix", matrix_type: Literal["G", "H"]
    ) -> "SystematicMatrix":
        """
        Создает систематическую матрицу на основе типа.
        """
        matrix_cls = cls._registry.get(matrix_type)

        rows, cols = matrix.matrix.shape
        columns_to_delete = [
            i for i in range(cols) if np.sum(matrix.matrix[:, i] == 1) == 1
        ]
        matrix_reduced = np.delete(matrix.matrix, columns_to_delete, axis=1)
        identity_matrix = np.eye(rows, dtype=int)

        if matrix_type in ("G", "generator", "порождающая"):
            result = np.hstack((identity_matrix, matrix_reduced)).tolist()
        elif matrix_type in ("H", "checks", "проверочная"):
            result = np.hstack((matrix_reduced, identity_matrix)).tolist()
        else:
            raise ValueError(
                f"Неправильный тип матрицы {matrix_cls}. Используйте 'G' или 'H'."
            )

        Registry.log(f"{matrix_cls.__name__}", result)
        return matrix_cls(result)
