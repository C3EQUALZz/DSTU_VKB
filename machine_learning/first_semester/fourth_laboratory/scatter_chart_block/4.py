"""
4. Как увеличить размер точек разброса в Matplotlib?
"""
from dataclasses import dataclass, field
from random import randint, choice
import matplotlib.pyplot as plt


@dataclass
class Dot:
    x: int = field(default_factory=lambda: randint(1, 100))
    y: int = field(default_factory=lambda: randint(1, 100))
    size: int = field(default_factory=lambda: randint(40, 100))


def draw_scatter_and_change_size_of_dot(*args: Dot) -> None:
    x_values = [dot.x for dot in args]
    y_values = [dot.y for dot in args]
    sizes = [dot.size for dot in args]

    plt.scatter(x_values, y_values, s=sizes, label=f'Точки')
    plt.legend()
    plt.show()


def main() -> None:
    draw_scatter_and_change_size_of_dot(
        Dot(),
        Dot(),
        Dot(),
        Dot()
    )


if __name__ == '__main__':
    main()