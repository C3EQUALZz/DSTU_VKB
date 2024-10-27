"""
Создать вектор размера 1n, заполенный нулями, но пятый элемент равен 1
"""
import numpy as np


def create_vector(n: int) -> np.array:
    arr = np.zeros(n, dtype=int)
    arr[4] = 1
    return arr


def main() -> None:
    user_input = input("Введите n: ")

    if user_input.isdigit():
        print(create_vector(int(f"1{user_input}")))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
