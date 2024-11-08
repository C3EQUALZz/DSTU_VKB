from typing import Union
import numpy as np
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.base import Matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
    GSystematicMatrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.verification_matrix import \
    HSystematicMatrix


class MatrixFactory:
    @staticmethod
    def create_systematic_matrix(matrix: "Matrix", matrix_type: str) -> Union["GSystematicMatrix", "HSystematicMatrix"]:
        """
        Создает систематическую матрицу на основе типа.
        """
        rows, cols = matrix.matrix.shape
        columns_to_delete = [i for i in range(cols) if np.sum(matrix.matrix[:, i] == 1) == 1]
        matrix_reduced = np.delete(matrix.matrix, columns_to_delete, axis=1)
        identity_matrix = np.eye(rows, dtype=int)

        if matrix_type == "G":
            return GSystematicMatrix(np.hstack((identity_matrix, matrix_reduced)).tolist())
        if matrix_type == "H":
            return HSystematicMatrix(np.hstack((matrix_reduced, identity_matrix)).tolist())
        raise ValueError("Invalid matrix type. Use 'G' or 'H'.")

    @staticmethod
    def create_inverse_matrix(matrix: "Matrix", matrix_type: str) -> Union["HSystematicMatrix", "GSystematicMatrix"]:
        if matrix_type == "G":
            n = matrix.shape[1]
            k = matrix.shape[0]
            return HSystematicMatrix(np.hstack((matrix.transpose(), np.eye(n - k))).tolist())

        if matrix_type == "H":
            res = np.hstack((np.eye(matrix.shape[1] - matrix.shape[0]), matrix.transpose())).tolist()
            return GSystematicMatrix(res)

