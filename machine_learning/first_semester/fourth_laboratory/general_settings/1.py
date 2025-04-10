"""
1. Как изменить прозрачность графика в Matplotlib с помощью Python?
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


def draw_vertical_line_and_change_transparency(line: Line) -> None:
    plt.axvline(
        x=line.level,
        color=line.color,
        linestyle=line.line_style,
        linewidth=line.line_width,
        alpha=0.1,
    )
    plt.show()


def main() -> None:
    draw_vertical_line_and_change_transparency(Line())


if __name__ == "__main__":
    main()
