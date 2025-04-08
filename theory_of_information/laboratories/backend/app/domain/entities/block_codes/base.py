from typing import List, Tuple, AnyStr
from abc import ABC, abstractmethod
import numpy as np


class Matrix(ABC):
    def __init__(self, matrix: List[List[int]]) -> None:
        self.matrix = np.array(matrix)

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.matrix.shape

    @property
    def n(self) -> int:
        return self.matrix.shape[1]

    @property
    def k(self) -> int:
        return self.matrix.shape[0]

    def __len__(self) -> int:
        return len(self.matrix)

    def __getitem__(self, key) -> "Matrix":
        return Matrix(self.matrix[key].tolist())

    def __str__(self) -> AnyStr:
        return "\n".join(str(row) for row in self.matrix)

    def to_systematic_form(self) -> "SystematicMatrix":
        raise NotImplementedError

    def transpose(self) -> "Matrix":
        return Matrix(self.matrix.transpose().tolist())


class SystematicMatrix(Matrix, ABC):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    @abstractmethod
    def find_another_type_matrix(self) -> "SystematicMatrix":
        raise NotImplemented()
