"""
4. Используйте несколько столбцов в легенде Matplotlib
"""

import numpy as np
from dataclasses import dataclass, field

from matplotlib import pyplot as plt

np.random.seed(1)


@dataclass
class Pair:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))


def draw_and_make_few_columns(first_pair_of_points: Pair, second_pair_of_points: Pair) -> None:
    plt.plot(first_pair_of_points.x, first_pair_of_points.y, color='blue', label='Первый график')
    plt.plot(second_pair_of_points.x, second_pair_of_points.y, color='red', label='Второй график')
    plt.legend(ncol=2)
    plt.show()


def main() -> None:
    draw_and_make_few_columns(Pair(), Pair())


if __name__ == '__main__':
    main()