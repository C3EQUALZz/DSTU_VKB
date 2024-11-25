"""
7. Как разместить легенду за пределами сюжета в Matplotlib?
"""
from dataclasses import dataclass, field
from enum import IntEnum
from itertools import count
from random import choice

import matplotlib.pyplot as plt
import numpy as np

counter = count(1)


class Position(IntEnum):
    Optimal = 0
    UpperRight = 1
    UpperLeft = 2
    LowerLeft = 3
    LowerRight = 4


@dataclass
class Line:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))
    color: str = field(default_factory=lambda: choice(('red', 'green', 'blue')))
    name: str = field(default_factory=lambda: f"{next(counter)} график")


def draw_and_place_legend_beyond_plot(*args: Line) -> None:
    for line in args:
        plt.plot(line.x, line.y, color=line.color, label=line.name)

    plt.legend(loc=Position.Optimal, bbox_to_anchor=(1, 0.5))
    plt.show()


def main() -> None:
    draw_and_place_legend_beyond_plot(Line())


if __name__ == '__main__':
    main()
