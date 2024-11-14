"""
3. Как создать точечную диаграмму с несколькими цветами в Matplotlib?
"""
from dataclasses import dataclass, field
from random import randint, choice
import matplotlib.pyplot as plt


@dataclass
class Dot:
    x: int = field(default_factory=lambda: randint(1, 100))
    y: int = field(default_factory=lambda: randint(1, 100))
    color: str = field(default_factory=lambda: choice(('red', 'blue', 'green', 'yellow', 'black')))


def draw_scatter_and_add_color_for_each_dot(*args: Dot) -> None:
    for dot in args:
        plt.scatter(dot.x, dot.y, c=dot.color, label=f'Точка x={dot.x}, y={dot.y}')

    plt.legend()
    plt.show()


def main() -> None:
    draw_scatter_and_add_color_for_each_dot(Dot(), Dot(), Dot(), Dot())


if __name__ == '__main__':
    main()
