"""
1. Как добавить легенду к точечной диаграмме в Matplotlib?
"""
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from random import randint


@dataclass
class Dot:
    x: int = field(default_factory=lambda: randint(1, 100))
    y: int = field(default_factory=lambda: randint(1, 100))


def draw_scatters_and_add_legend(*args: Dot) -> None:
    x_values = [dot.x for dot in args]
    y_values = [dot.y for dot in args]

    plt.scatter(x_values, y_values, label=f'Точки')

    plt.legend()
    plt.show()


def main() -> None:
    draw_scatters_and_add_legend(Dot(), Dot(), Dot(), Dot(), Dot())


if __name__ == '__main__':
    main()
