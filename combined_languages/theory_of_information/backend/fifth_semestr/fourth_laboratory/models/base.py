from typing import List
import numpy as np

class Matrix:
    def __init__(self, matrix: List[List[int]]) -> None:
        self.matrix = np.array(matrix)

    def transpose(self) -> "Matrix":
        return np.transpose(self.matrix)

    def multiply(self, other_matrix):
        # Multiply the matrix with another matrix
        pass