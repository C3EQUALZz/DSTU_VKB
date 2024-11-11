"""
7. Как разместить легенду за пределами сюжета в Matplotlib?
"""
from dataclasses import dataclass, field
import numpy as np
from enum import IntEnum
import matplotlib.pyplot as plt


class Position(IntEnum):
    Optimal = 0
    UpperRight = 1
    UpperLeft = 2
    LowerLeft = 3
    LowerRight = 4


@dataclass
class Pair:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))


def draw_and_place_legend_beyond_plot(pair_of_coords: Pair) -> None:
    plt.plot(pair_of_coords.x, pair_of_coords.y, label='График 1')
    plt.legend(loc=Position.Optimal, bbox_to_anchor=(1, 0.5))
    plt.show()


def main() -> None:
    draw_and_place_legend_beyond_plot(Pair())


if __name__ == '__main__':
    main()
