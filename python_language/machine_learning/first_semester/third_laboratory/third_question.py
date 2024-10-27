"""
Создать массив n x n x n со случайными значениями
"""
import numpy as np


def create_array(n: int) -> np.array:
    return np.random.randn(n, n, n)


def main() -> None:
    user_input = input('Введите число: ')

    if user_input.isdigit():
        print(create_array(int(user_input)))
    else:
        print('Вы ввели не число')


if __name__ == '__main__':
    main()
