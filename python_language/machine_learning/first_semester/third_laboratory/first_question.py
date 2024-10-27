"""
Найти индексы ненулевых элементов в заданном массиве
"""
import numpy as np


# np.where возвращает почему-то кортеж, поэтому тут индексация с 0 получается

def find_non_nullable(arr: np.array) -> np.array:
    return np.where(arr != 0)[0]


def main() -> None:
    arr = np.array(np.random.randint(-5, 5, 10))
    print(f"Изначальный массив: {arr}")
    print(f"Индексы ненулевых элементов: {find_non_nullable(arr)}")


if __name__ == '__main__':
    main()
