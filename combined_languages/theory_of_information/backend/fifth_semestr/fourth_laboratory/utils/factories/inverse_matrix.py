from typing import TYPE_CHECKING, Literal

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    RegistryFactory
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import \
        SystematicMatrix


class InverseMatrixFactory(RegistryFactory):

    @classmethod
    def create(cls, matrix: Matrix, matrix_type: Literal["G", "H"]) -> "SystematicMatrix":
        matrix_cls = cls._registry.get(matrix_type)

        n = matrix.shape[1]
        k = matrix.shape[0]

        if matrix_type == "G":
            required_columns = matrix[:, -(n - k):].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((required_columns, eye_matrix)).tolist()

        elif matrix_type == "H":
            required_columns = matrix[:, :(n - k)].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((eye_matrix, required_columns)).tolist()

        else:
            raise ValueError(f"Неизвестный тип матрицы: {matrix_type}")

        Registry.log(f"Параметр k {matrix_cls.__name__}", k)
        Registry.log(f"Параметр n {matrix_cls.__name__}", n)
        Registry.log(f"Обратная матрица: {matrix_cls.__name__}", new_matrix)

        return matrix_cls(new_matrix)
