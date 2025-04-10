"""
1. Нарисуйте горизонтальную гистограмму с помощью Matplotlib
"""

import string
from dataclasses import dataclass, field
from random import choice, randint

import matplotlib.pyplot as plt


@dataclass
class Column:
    data: int = field(default_factory=lambda: randint(0, 100))
    name: str = field(default_factory=lambda: f"{choice(string.ascii_uppercase)}")


def draw_horizontal_histograms(*args: Column) -> None:
    for column in args:
        plt.barh(column.name, column.data)
    plt.show()


def main() -> None:
    draw_horizontal_histograms(Column(), Column(), Column(), Column())


if __name__ == "__main__":
    main()
