"""
Развернуть одномерный массив (первый становится последним)
"""
import numpy as np


def expand_array(arr: np.ndarray[int]) -> np.ndarray[int]:
    return arr[::-1]


def main() -> None:
    arr = np.random.randint(0, 10, 10)
    print(f"Изначальный массив: {arr}")
    print(f"Развернутый массив: {expand_array(arr)}")


if __name__ == '__main__':
    main()
