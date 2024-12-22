"""
Умножьте матрицу размерности (5, 3) на (3, 2)
"""
import numpy as np


def multiply(a: np.array, b: np.array) -> np.array:
    return np.dot(a, b)


def main() -> None:
    print(
        'Матрица 5x3: ',
        arr1 := np.random.randint(0, 10, (5, 3)),
        "\nМатрица 3x2: ",
        arr2 := np.random.randint(0, 10, (3, 2)),
        "\nПосле умножения: ",
        multiply(arr1, arr2),
        sep='\n'
    )


if __name__ == '__main__':
    main()
