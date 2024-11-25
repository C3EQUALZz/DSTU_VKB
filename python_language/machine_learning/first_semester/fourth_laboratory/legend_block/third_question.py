"""
3. Как изменить расстояние по вертикали между записями легенды в Matplotlib?
"""
from dataclasses import dataclass, field
from itertools import count
from random import choice

import numpy as np
from matplotlib import pyplot as plt

np.random.seed(1)

counter = count(1)


@dataclass
class Line:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))
    color: str = field(default_factory=lambda: choice(('red', 'green', 'blue')))
    name: str = field(default_factory=lambda: f"{next(counter)} график")

def draw_and_change_vertical_distance(*args: Line) -> None:
    for line in args:
        plt.plot(line.x, line.y, color=line.color, label=line.name)
    plt.legend(labelspacing=2)
    plt.show()


def main() -> None:
    draw_and_change_vertical_distance(*(Line() for _ in range(3)))


if __name__ == '__main__':
    main()
