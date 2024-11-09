from importlib import import_module
from typing import TYPE_CHECKING

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.factories.base import \
    Factory

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import \
        SystematicMatrix

PATH_TO_MODELS = "combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models."


class InverseMatrixFactory(Factory):
    _registry = {}

    # NOTE: я не придумал как сделать нормально без динамического импорта.
    # У Python есть проблема с циклическими импортами. В случае бы GSystematic и Hsystematic просто импортировали бы друг друга, а это плохо
    @classmethod
    def register(cls, matrix_type: str, matrix_class_name: str) -> None:
        module_name, class_name = (PATH_TO_MODELS + matrix_class_name).rsplit('.', 1)
        matrix_class = getattr(import_module(module_name), class_name)
        cls._registry[matrix_type] = matrix_class

    @classmethod
    def create(cls, matrix: Matrix, matrix_type: str) -> "SystematicMatrix":
        matrix_cls = cls._registry.get(matrix_type)

        if not matrix_cls:
            raise ValueError(f"Unknown matrix type: {matrix_type}")

        n = matrix.shape[1]
        k = matrix.shape[0]

        if matrix_type == "G":
            required_columns = matrix[:, -(n - k):].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((required_columns, eye_matrix)).tolist()
            return matrix_cls(new_matrix)
        if matrix_type == "H":
            required_columns = matrix[:, :(n - k)].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((eye_matrix, required_columns)).tolist()
            return matrix_cls(new_matrix)
