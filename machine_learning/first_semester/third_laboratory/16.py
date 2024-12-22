"""
Создайте матрицу (5, 5), заполненую от 0 до 6
"""
import numpy as np


def main() -> None:
    print("Матрица 5x5: ", np.random.randint(0, 7, (5, 5)), sep="\n")


if __name__ == '__main__':
    main()
