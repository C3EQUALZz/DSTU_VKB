"""
2. Как соединить точки диаграммы рассеяния с линией в Matplotlib?
"""

from dataclasses import dataclass, field
from random import randint

import matplotlib.pyplot as plt


@dataclass
class Dot:
    x: int = field(default_factory=lambda: randint(1, 100))
    y: int = field(default_factory=lambda: randint(1, 100))


def draw_scatters_and_connect_them(*args: Dot) -> None:
    x_values = [dot.x for dot in args]
    y_values = [dot.y for dot in args]

    plt.scatter(x_values, y_values, label="Точки", color="blue")

    plt.plot(x_values, y_values, label="Линия", color="red")

    plt.legend()
    plt.show()


def main() -> None:
    draw_scatters_and_connect_them(Dot(), Dot(), Dot(), Dot(), Dot())


if __name__ == "__main__":
    main()
