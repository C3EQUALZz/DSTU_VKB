"""
1. Постройте горизонтальную линию в Matplotlib (использовать plt.axhline)
"""
import matplotlib.pyplot as plt


def draw_horizontal_line(point: int) -> None:
    plt.axhline(y=point)
    plt.show()


def main() -> None:
    point = 2
    draw_horizontal_line(point)


if __name__ == '__main__':
    main()
