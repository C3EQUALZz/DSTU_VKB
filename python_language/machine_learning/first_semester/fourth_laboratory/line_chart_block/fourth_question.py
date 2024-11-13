"""
4. Постройте несколько вертикальных линий разных типов, ширины и цветов на одном графике
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


def draw_several_vertical_lines(*args: Line) -> None:
    for line in args:
        plt.axvline(x=line.level, color=line.color, linestyle=line.line_style, linewidth=line.line_width)

    plt.show()


def main() -> None:
    draw_several_vertical_lines(Line(), Line(), Line())


if __name__ == '__main__':
    main()
