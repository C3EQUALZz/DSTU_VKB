"""
Создайте матрицу (10, 10) так, чтобы на границе были 0, а внтури 1
"""
import numpy as np


def fill_matrix(matrix: np.ndarray[np.ndarray[int]]) -> np.ndarray[np.ndarray[int]]:
    matrix[1:-1, 1:-1] = 1
    return matrix


def main() -> None:
    arr = np.zeros((10, 10), dtype=int)

    print("Матрица 10x10: ", fill_matrix(arr), sep='\n')


if __name__ == '__main__':
    main()
