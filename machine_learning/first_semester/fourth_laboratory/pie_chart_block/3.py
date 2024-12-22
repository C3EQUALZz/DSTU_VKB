"""
3. Радиально сместите клин круговой диаграммы в Matplotlib
"""

import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from random import randint, choice, random
import string


@dataclass
class Piece:
    size: int = field(default_factory=lambda: randint(10, 50))
    label: str = field(default_factory=lambda: f"Категория - {choice(string.ascii_uppercase)}")
    explode: int = field(default_factory=lambda: random())


def draw_pie_chart_and_shift_the_wedge(*args: Piece) -> None:
    labels = [piece.label for piece in args]
    sizes = [piece.size for piece in args]
    explodes = [piece.explode for piece in args]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explodes)
    plt.show()


def main() -> None:
    draw_pie_chart_and_shift_the_wedge(Piece(), Piece(), Piece(), Piece(), Piece())


if __name__ == '__main__':
    main()
