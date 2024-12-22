"""
Найти ближайшее к заданному значению число в заданном массиве
"""
import numpy as np


def find_approximate(m: np.array, a: int) -> np.array:
    return (np.abs(m - a)).argmin()


def main() -> None:

    user_input = input('Введите число n - количество элементов массива: ')

    if not user_input.isdigit():
        print("Вы ввели не число")
        exit()

    n = int(user_input)
    arr = np.random.randint(1, 10, n)
    print(f"Массив случайных чисел: {arr}")

    user_input = input('Введите число a: ')

    if not user_input.isdigit():
        print("Вы ввели не число")
        exit()

    print(find_approximate(arr, int(user_input)))


if __name__ == '__main__':
    main()
