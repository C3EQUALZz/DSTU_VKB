"""
Отнять среднее из каждой строки в матрице
"""
import numpy as np


def substrate_mean(arr: np.array) -> tuple[np.array, np.array]:
    return (arr.mean(axis=1)).reshape(-1, 1), (arr.T - arr.mean(axis=1)).T


def main() -> None:
    arr = np.random.randint(0, 10, (3, 3))
    mean, result = substrate_mean(arr)
    print("Массив", arr, "Среднее", mean, "Результат", result, sep='\n')


if __name__ == '__main__':
    main()
