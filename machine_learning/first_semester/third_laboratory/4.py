"""
Создать вектор (одномерный массив) размера n, заполненный нулями
"""
import numpy as np


def create_vector(n: int) -> np.ndarray[np.ndarray[int]]:
    return np.zeros(n, dtype=int)


def main() -> None:
    user_input = input('Введите число: ')

    if user_input.isdigit():
        print(create_vector(int(user_input)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
