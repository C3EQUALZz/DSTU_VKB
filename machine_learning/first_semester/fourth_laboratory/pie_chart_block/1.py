"""
1. Постройте круговую диаграмму в Python, используя Matplotlib
"""
import string
from dataclasses import dataclass, field
from random import randint, choice

import matplotlib.pyplot as plt


@dataclass
class Piece:
    size: int = field(default_factory=lambda: randint(10, 50))
    label: str = field(default_factory=lambda: f"Категория - {choice(string.ascii_uppercase)}")


def draw_pie_chart(*args: Piece) -> None:
    labels = [piece.label for piece in args]
    sizes = [piece.size for piece in args]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.show()


def main() -> None:
    draw_pie_chart(
        Piece(),
        Piece(),
        Piece(),
        Piece(),
    )


if __name__ == '__main__':
    main()
