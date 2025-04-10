"""
15. Скрыть ось, границы и пробелы в Matplotlib
"""

from dataclasses import dataclass, field
from random import choice, randint

import matplotlib.pyplot as plt


@dataclass
class Line:
    level: int = field(default_factory=lambda: randint(1, 10))
    color: str = field(default_factory=lambda: choice(("r", "g", "b")))
    line_style: str = field(default_factory=lambda: choice(("--", ":", "-")))
    line_width: int = field(default_factory=lambda: randint(1, 5))


def draw_lines_and_hide_axis(*args: Line) -> None:
    for line in args:
        plt.axvline(
            x=line.level,
            color=line.color,
            linestyle=line.line_style,
            linewidth=line.line_width,
        )

    plt.axis("off")
    plt.margins(0)
    plt.show()


def main() -> None:
    draw_lines_and_hide_axis(
        Line(),
        Line(),
        Line(),
        Line(),
    )


if __name__ == "__main__":
    main()
