"""
8. Удалите границу легенды в Matplotlib
"""
from dataclasses import dataclass, field
from itertools import count
from random import choice

import matplotlib.pyplot as plt
import numpy as np

counter = count(1)


@dataclass
class Line:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))
    color: str = field(default_factory=lambda: choice(('red', 'green', 'blue')))
    name: str = field(default_factory=lambda: f"{next(counter)} график")


def draw_and_delete_border_legend(*args) -> None:
    for line in args:
        plt.plot(line.x, line.y, color=line.color, label=line.name)
    plt.legend(frameon=False)
    plt.show()


def main() -> None:
    draw_and_delete_border_legend(Line())


if __name__ == '__main__':
    main()