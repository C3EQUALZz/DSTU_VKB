"""
Определить, есть ли в двумерном массиве нулевые столбцы
"""
import numpy as np


def check_zero_column(arr: np.ndarray[np.ndarray[int]]) -> bool:
    return np.any(arr.sum(axis=0) == 0)


def main() -> None:
    arr = np.random.randint(0, 2, (2, 3))
    print("Матрица: ", arr,
          f"Есть ли в двумерном массиве нулевые столбцы: {('Нет', 'Да')[int(check_zero_column(arr))]}",
          sep='\n')


if __name__ == '__main__':
    main()
