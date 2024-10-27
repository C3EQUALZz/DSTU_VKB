"""
Дан четырехмерный массив, посчитать сумму по последним двум осям
"""
import numpy as np


def find_sum_last_two_axes(arr: np.array) -> np.array:
    return arr.reshape(arr.shape[:-2] + (-1,)).sum(axis=-1)


def main():
    arr = np.random.randint(1, 100, size=(2, 2, 2, 3))
    print('4-х мерный массив:', arr, "Сумма:", find_sum_last_two_axes(arr), sep="\n")


if __name__ == '__main__':
    main()
