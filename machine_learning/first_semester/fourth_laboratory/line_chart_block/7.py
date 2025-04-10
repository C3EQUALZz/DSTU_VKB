"""
7. Как заполнить между несколькими строками в Matplotlib?
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Sequence, cast

import matplotlib.pyplot as plt
import numpy as np


class Position(IntEnum):
    Optimal = 0
    UpperRight = 1
    UpperLeft = 2
    LowerLeft = 3
    LowerRight = 4


@dataclass
class Function:
    x: np.ndarray[int]
    y: np.ndarray[int]
    label: str


def draw_graphs_and_fill_the_space_between_them(*args: Function) -> None:
    for func in args:
        plt.plot(func.x, func.y, label=func.label)

    for i in range(len(args) - 1):
        first_function = args[i]
        second_function = args[i + 1]

        plt.fill_between(
            first_function.x,
            first_function.y,
            second_function.y,
            where=cast(Sequence[bool], (first_function.y > second_function.y)),
            color="lightblue",
            label=f"Область между {first_function.label} и {second_function.label}",
        )

        plt.fill_between(
            first_function.x,
            first_function.y,
            second_function.y,
            where=cast(Sequence[bool], (first_function.y < second_function.y)),
            color="lightgreen",
        )

    plt.legend(loc=Position.LowerLeft)
    plt.show()


def main() -> None:
    x = np.linspace(0, 10, 100)
    sinusoid = Function(x=x, y=np.sin(x), label="sin(x)")
    cosine = Function(x=x, y=np.cos(x), label="cos(x)")
    draw_graphs_and_fill_the_space_between_them(sinusoid, cosine)


if __name__ == "__main__":
    main()
