"""
Создать nxn матрицу и заполнить её в шахматном порядке
"""

import numpy as np


def create_matrix(n: int) -> np.array:
    rows, cols = np.indices((n, n))
    return (rows + cols) % 2


def main() -> None:
    user_input = input('Введите число n ')

    if user_input.isdigit():
        print(create_matrix(int(user_input)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
