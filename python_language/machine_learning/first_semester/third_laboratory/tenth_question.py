"""
Заменить максимальный элемент на ноль
"""
import numpy as np


def replace_max_to_zero(arr: np.ndarray[int]) -> np.ndarray[int]:
    arr[np.argmax(arr)] = 0
    return arr


def main() -> None:
    arr = np.random.randint(0, 10, 10)
    print(f"Изначальный массив: {arr}")
    print(f"После замены: {replace_max_to_zero(arr)}")


if __name__ == '__main__':
    main()
