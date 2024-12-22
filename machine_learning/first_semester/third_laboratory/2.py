"""
Создать n x n единичную матрицу
"""

import numpy as np


def create_ones(n: int) -> np.ndarray[int]:
    return np.ones((n, n), dtype=int)


def main() -> None:
    user_input = input("Введите число - размер матрицы единичной матрицы: ")

    if user_input.isdigit():
        print(create_ones(int(user_input)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
