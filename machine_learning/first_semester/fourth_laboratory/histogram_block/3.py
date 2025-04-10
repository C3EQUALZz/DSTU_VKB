"""
3. Как аннотировать столбцы в Barplot с помощью Matplotlib на Python?
"""

import string
from dataclasses import dataclass, field
from random import choice, randint

import matplotlib.pyplot as plt


@dataclass
class Column:
    data: int = field(default_factory=lambda: randint(0, 100))
    name: str = field(default_factory=lambda: f"{choice(string.ascii_uppercase)}")


def draw_bar_plot_and_annotate_each_column(*args: Column) -> None:
    names = [column.name for column in args]
    values = [column.data for column in args]

    bars = plt.barh(names, values)

    for bar in bars:
        plt.annotate(
            str(bar.get_width()),
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            va="center",
            ha="left",
        )

    plt.show()


def main() -> None:
    draw_bar_plot_and_annotate_each_column(
        Column(),
        Column(),
        Column(),
        Column(),
    )


if __name__ == "__main__":
    main()
