"""
2. Как установить границу для клиньев в круговой диаграмме Matplotlib?
"""

import string
from dataclasses import dataclass, field
from random import choice, randint

import matplotlib.pyplot as plt


@dataclass
class Piece:
    size: int = field(default_factory=lambda: randint(10, 50))
    label: str = field(
        default_factory=lambda: f"Категория - {choice(string.ascii_uppercase)}"
    )


def draw_pie_chart_and_set_the_edge(*args: Piece) -> None:
    labels = [piece.label for piece in args]
    sizes = [piece.size for piece in args]

    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        wedgeprops={"lw": 1, "ls": "-", "edgecolor": "k"},
    )
    plt.show()


def main() -> None:
    draw_pie_chart_and_set_the_edge(
        Piece(),
        Piece(),
        Piece(),
        Piece(),
    )


if __name__ == "__main__":
    main()
