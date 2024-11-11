"""
8. Удалите границу легенды в Matplotlib
"""
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Pair:
    x: np.ndarray[int] = field(default_factory=lambda: np.linspace(1, 50, 50, dtype=int))
    y: np.ndarray[int] = field(default_factory=lambda: np.random.randint(0, 20, 50))


def draw_and_delete_border_legend(pair_of_coords: Pair) -> None:
    plt.plot(pair_of_coords.x, pair_of_coords.y, color='blue', label="График")
    plt.legend(frameon=False)
    plt.show()


def main() -> None:
    draw_and_delete_border_legend(Pair())


if __name__ == '__main__':
    main()
