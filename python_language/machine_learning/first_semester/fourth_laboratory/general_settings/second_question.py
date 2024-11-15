"""
2. Как изменить цвет графика в Matplotlib с помощью Python?
"""

"""
1. Как изменить прозрачность графика в Matplotlib с помощью Python?
"""
from dataclasses import dataclass, field
from random import randint, choice

import matplotlib.pyplot as plt


@dataclass
class Line:
    level: int = field(default_factory=lambda: randint(1, 10))
    color: str = field(default_factory=lambda: choice(('r', 'g', 'b')))


def draw_vertical_line_and_change_transparency(line: Line) -> None:
    plt.axvline(x=line.level, color=line.color)
    plt.show()


def main() -> None:
    draw_vertical_line_and_change_transparency(Line())


if __name__ == '__main__':
    main()
