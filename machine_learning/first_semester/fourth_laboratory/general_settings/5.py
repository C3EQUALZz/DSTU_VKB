"""
5. Как задать цвет фона графика в Matplotlib?
"""
from dataclasses import dataclass, field
from random import randint, choice

import matplotlib.pyplot as plt


@dataclass
class Line:
    level: int = field(default_factory=lambda: randint(1, 10))
    color: str = field(default_factory=lambda: choice(('r', 'g', 'b')))
    line_style: str = field(default_factory=lambda: choice(('--', ':', '-')))
    line_width: int = field(default_factory=lambda: randint(1, 5))


def draw_lines_and_set_background_color(*args: Line) -> None:
    for line in args:
        plt.axvline(x=line.level, color=line.color, linestyle=line.line_style, linewidth=line.line_width)

    plt.gca().set_facecolor('lightgrey')
    plt.show()


def main() -> None:
    draw_lines_and_set_background_color(
        Line(),
        Line(),
        Line(),
        Line()
    )


if __name__ == '__main__':
    main()