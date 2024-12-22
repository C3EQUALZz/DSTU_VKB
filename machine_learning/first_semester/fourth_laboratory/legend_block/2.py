"""
2. Как изменить размер шрифта легенды в Matplotlib?
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)

def draw_and_change_font_size(x: np.ndarray[int], y: np.ndarray[int]) -> None:
    plt.plot(x, y, label="График")
    plt.legend(fontsize='22')
    plt.show()


def main() -> None:
    x = np.linspace(1, 50, 50, dtype=int)
    y = np.random.randint(0, 20, 50)
    draw_and_change_font_size(x, y)


if __name__ == '__main__':
    main()
