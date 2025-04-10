"""
Дан двумерный массив и два числа: i и j. Поменяйте в массиве столбцы с номерами i и j.
"""

from pprint import pprint

import numpy as np


def solution():
    matrix = np.random.randint(1000, size=tuple(map(int, input().split())))
    pprint(matrix)
    i, j = map(int, input().split())

    matrix[:, [i, j]] = matrix[:, [j, i]]
    pprint(matrix)


if __name__ == "__main__":
    solution()
