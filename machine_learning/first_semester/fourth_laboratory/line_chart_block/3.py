"""
3. Постройте вертикальную линию в Matplotlib
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


def draw_vertical_line(line: Line) -> None:
    plt.axvline(
        x=line.level,
        color=line.color,
        linestyle=line.line_style,
        linewidth=line.line_width,
    )
    plt.show()


def main() -> None:
    draw_vertical_line(Line())


if __name__ == "__main__":
    main()
