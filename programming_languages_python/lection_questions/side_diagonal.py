"""
 Дано число n. Создайте массив размером n×n и заполните его по следующему правилу:

Числа на диагонали, идущей из правого верхнего в левый нижний угол равны 1.

Числа, стоящие выше этой диагонали, равны 0.

Числа, стоящие ниже этой диагонали, равны 2.

Полученный массив выведите на экран. Числа в строке разделяйте одним пробелом.
"""

from pprint import pprint

import numpy as np


def solution():
    sizes = tuple(map(int, input().split()))
    matrix = np.array(
        [
            [
                2 if j > sizes[0] - i - 1 else 1 if j == sizes[0] - i - 1 else 0
                for i in range(sizes[0])
            ]
            for j in range(sizes[1])
        ]
    )
    pprint(matrix)


if __name__ == "__main__":
    solution()
