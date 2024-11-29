"""
6. Как вручную добавить легенду с цветной рамкой на фигуру Matplotlib?
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


def draw_and_add_color_frame_figure(*args: Line) -> None:
    for line in args:
        plt.plot(line.x, line.y, color=line.color, label=line.name)

    legend = plt.legend()
    frame = legend.get_frame()
    frame.set_edgecolor('red')
    frame.set_linewidth(2)

    plt.show()


def main() -> None:
    draw_and_add_color_frame_figure(Line())


if __name__ == '__main__':
    main()
