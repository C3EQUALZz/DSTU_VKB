"""
Создать матрицу с 0 внутри, и 1 на границах
"""
import numpy as np


def create_matrix(n: int) -> np.array:
    arr = np.ones((n, n), dtype=int)
    arr[1:-1, 1:-1] = 0
    return arr


def main() -> None:
    user_choice = input('Введите число n ')

    if user_choice.isdigit():
        print(create_matrix(int(user_choice)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
