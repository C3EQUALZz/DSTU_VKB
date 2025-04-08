import logging
from typing import TYPE_CHECKING, Literal

import numpy as np

from app.domain.entities.block_codes.factories.base import RegistryFactory

if TYPE_CHECKING:
    from app.domain.entities.block_codes.base import Matrix, SystematicMatrix

logger = logging.getLogger(__name__)


class InverseMatrixFactory(RegistryFactory):
    @classmethod
    def create(cls, matrix: "Matrix", matrix_type: Literal["G", "H"]) -> "SystematicMatrix":
        matrix_cls = cls._registry.get(matrix_type)

        n = matrix.shape[1]
        k = matrix.shape[0]

        if matrix_type == "G":
            logger.info("Параметр k GSystematicMatrix: %s", len(matrix[0]))
            logger.info("Параметр n GSystematicMatrix: %s", len(matrix))
            required_columns = matrix[:, -(n - k):].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((required_columns, eye_matrix)).tolist()

        elif matrix_type == "H":
            logger.info("Параметр k HSystematicMatrix: %s", len(matrix[0]))
            logger.info("Параметр n HSystematicMatrix: %s", len(matrix))
            required_columns = matrix[:, :(n - k)].transpose().matrix
            eye_matrix = np.eye(n - k, dtype=required_columns.dtype)
            new_matrix = np.hstack((eye_matrix, required_columns)).tolist()

        else:
            raise ValueError(f"Неизвестный тип матрицы: {matrix_type}")

        logger.info("Параметр k %s %s", matrix_cls.__name__, len(new_matrix))
        logger.info("Параметр n %s %s", matrix_cls.__name__, len(new_matrix[0]))
        logger.info("Обратная матрица: %s %s", matrix_cls.__name__, new_matrix)

        return matrix_cls(new_matrix)
