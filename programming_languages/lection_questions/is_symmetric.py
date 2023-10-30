"""
Дано число n и массив размером n×n. Проверьте, является ли этот массив симметричным относительно главной диагонали.
Выведите слово “YES”, если массив симметричный, и слово “NO” в противном случае.
"""
import numpy as np


def is_symmetric():
    matrix = np.array([[0, 1, 2],
                       [1, 2, 3],
                       [2, 3, 4]])
    n, m = matrix.shape
    print(("NO", "YES")[all(matrix[i, j] == matrix[j, i] for i in range(n) for j in range(m))])
