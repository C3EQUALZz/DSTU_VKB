"""
7. Добавьте текст внутри графика в Matplotlib
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


def draw_line_and_add_text_in_function(line: Line) -> None:
    plt.axvline(
        x=line.level,
        color=line.color,
        linestyle=line.line_style,
        linewidth=line.line_width
    )

    plt.text(
        x=line.level,
        y=5,
        s="Огромный текст",
        ha='center'
    )

    plt.ylim(0, 10)
    plt.show()


def main() -> None:
    draw_line_and_add_text_in_function(Line())


if __name__ == '__main__':
    main()
