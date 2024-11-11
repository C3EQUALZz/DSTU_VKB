"""
1. Измените положение легенды в Matplotlib
"""
import matplotlib.pyplot as plt
import numpy as np
from enum import IntEnum

np.random.seed(1)


class Position(IntEnum):
    Optimal = 0
    UpperRight = 1
    UpperLeft = 2
    LowerLeft = 3
    LowerRight = 4


def draw(x: np.ndarray[int], y: np.ndarray[int]) -> None:
    plt.plot(x, y, label="График")
    plt.legend(loc=Position.Optimal)
    plt.show()


def main() -> None:
    x = np.linspace(1, 50, 50, dtype=int)
    y = np.random.randint(0, 20, 50)
    draw(x, y)


if __name__ == '__main__':
    main()
