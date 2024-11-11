"""
6. Как вручную добавить легенду с цветной рамкой на фигуру Matplotlib?
"""
import numpy as np
from dataclasses import dataclass, field
import matplotlib.pyplot as plt


@dataclass
class Pair:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))


def draw_and_add_color_frame_figure(first_pair_of_points: Pair) -> None:
    plt.plot(first_pair_of_points.x, first_pair_of_points.y, color="blue", label='Жесточайший график')
    legend = plt.legend()
    frame = legend.get_frame()
    frame.set_edgecolor('red')
    frame.set_linewidth(2)

    plt.show()


def main() -> None:
    draw_and_add_color_frame_figure(Pair())


if __name__ == '__main__':
    main()
