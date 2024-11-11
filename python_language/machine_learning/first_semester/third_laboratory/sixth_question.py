"""
Создать вектор со значениями от n до m
"""

import numpy as np


def create_vector(n: int, m: int) -> np.ndarray[int]:
    return np.arange(n, m)


def main() -> None:
    n, m = input("Введите два значения через пробел: ").strip().split()

    if n.isdigit() and m.isdigit():
        print(create_vector(int(n), int(m)))
    else:
        print("Вы ввели не числа")


if __name__ == '__main__':
    main()
