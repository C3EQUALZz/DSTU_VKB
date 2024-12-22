"""
10. Как изменить размер фигур, нарисованных с помощью matplotlib?
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import randint, choice, random

import matplotlib.pyplot as plt


class Shape(ABC):
    @abstractmethod
    def draw(self) -> None:
        ...


@dataclass
class Circle(Shape):
    x: float = field(default_factory=lambda: random())
    y: float = field(default_factory=lambda: random())
    size: int = field(default_factory=lambda: randint(50, 200))
    color: str = field(default_factory=lambda: choice(('red', 'green', 'blue')))
    label: str = "Круг"

    def draw(self) -> None:
        plt.scatter(self.x, self.y, s=self.size, c=self.color, marker='o', label=self.label)


@dataclass
class Square(Shape):
    x: float = field(default_factory=lambda: random())
    y: float = field(default_factory=lambda: random())
    size: float = field(default_factory=lambda: random())
    line_width: float = field(default_factory=lambda: randint(1, 5))
    label: str = 'Квадрат'

    def draw(self):
        # Рисуем квадрат
        plt.plot(
            [
                self.x - self.size / 2,
                self.x + self.size / 2,
                self.x + self.size / 2,
                self.x - self.size / 2,
                self.x - self.size / 2
            ],
            [
                self.y - self.size / 2,
                self.y - self.size / 2,
                self.y + self.size / 2,
                self.y + self.size / 2,
                self.y - self.size / 2
            ],
            linewidth=self.line_width,
            label=self.label
        )


def draw_shapes_and_change_sizes(*args: Shape) -> None:
    for shape in args:
        shape.draw()

    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.gca().set_aspect('equal', adjustable='box')  # Сохраняем пропорции
    plt.show()


def main() -> None:
    draw_shapes_and_change_sizes(Circle(), Square())


if __name__ == '__main__':
    main()
