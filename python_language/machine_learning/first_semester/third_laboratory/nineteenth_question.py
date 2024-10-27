"""
Для заданного числа найдите ближайший к нему элемент в векторе
"""
import numpy as np


def find_nearest(array: np.array, value: int) -> int:
    return (np.abs(array - value)).argmin()


def main() -> None:
    size = input("Введите размерность вектора (от 1 до n): ")

    if size.isdigit():
        size = int(size)
    else:
        print("Вы ввели не число")
        exit()

    array = np.random.randint(1, 10, size)

    print("Вектор, наполненный случайными числами: ", array, sep="\n")

    value = input("Введите число, относительно которого хотите найти ближайшее: ")

    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        value = int(value)
    else:
        print("Вы ввели не число")
        exit()

    print(f"Индекс элемента: {find_nearest(array, value)}")


if __name__ == '__main__':
    main()
