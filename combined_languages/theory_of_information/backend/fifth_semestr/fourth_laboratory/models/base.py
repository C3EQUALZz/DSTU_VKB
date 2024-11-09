from typing import List

import numpy as np


class Matrix:
    def __init__(self, matrix: List[List[int]]) -> None:
        self.matrix = np.array(matrix)

    def to_systematic_form(self) -> "SystematicMatrix":
        raise NotImplementedError

    def transpose(self) -> "Matrix":
        return Matrix(self.matrix.transpose().tolist())

    def __len__(self) -> int:
        return len(self.matrix)

    @property
    def shape(self) -> tuple[int, ...]:
        return self.matrix.shape

    def __getitem__(self, key) -> "Matrix":
        return Matrix(self.matrix[key].tolist())

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.matrix)


class SystematicMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def find_another_type_matrix(self) -> "SystematicMatrix":
        raise NotImplemented()

    @property
    def n(self) -> int:
        return self.matrix.shape[1]

    @property
    def k(self) -> int:
        return self.matrix.shape[0]
