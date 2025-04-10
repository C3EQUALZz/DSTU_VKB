"""
11. Как вручную добавить легенду с цветной рамкой на фигуру Matplotlib?
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice, randint, random

import matplotlib.pyplot as plt


class Shape(ABC):
    @abstractmethod
    def draw(self) -> None: ...


@dataclass
class Circle(Shape):
    x: float = field(default_factory=lambda: random())
    y: float = field(default_factory=lambda: random())
    size: int = field(default_factory=lambda: randint(50, 200))
    color: str = field(default_factory=lambda: choice(("red", "green", "blue")))
    label: str = "Круг"

    def draw(self) -> None:
        plt.scatter(
            self.x, self.y, s=self.size, c=self.color, marker="o", label=self.label
        )


@dataclass
class Square(Shape):
    x: float = field(
        default_factory=lambda: random()
    )  # Случайное значение от 0.1 до 1.0
    y: float = field(
        default_factory=lambda: random()
    )  # Случайное значение от 0.1 до 1.0
    size: float = field(
        default_factory=lambda: randint(1, 5) / 10
    )  # Случайный размер от 0.1 до 0.5
    line_width: float = field(
        default_factory=lambda: randint(1, 5)
    )  # Случайная толщина линии от 1 до 5
    label: str = field(default_factory=lambda: "Квадрат")

    def draw(self) -> None:
        # Рисуем квадрат
        plt.plot(
            [
                self.x - self.size / 2,
                self.x + self.size / 2,
                self.x + self.size / 2,
                self.x - self.size / 2,
                self.x - self.size / 2,
            ],
            [
                self.y - self.size / 2,
                self.y - self.size / 2,
                self.y + self.size / 2,
                self.y + self.size / 2,
                self.y - self.size / 2,
            ],
            linewidth=self.line_width,
            label=self.label,
        )


def draw_shapes_and_add_colorful_legend(*args: Shape) -> None:
    for shape in args:
        shape.draw()

    legend = plt.legend()
    frame = legend.get_frame()
    frame.set_facecolor("lightgray")  # Цвет фона рамки
    frame.set_edgecolor("blue")  # Цвет рамки
    frame.set_linewidth(2)  # Толщина рамки

    # Отображение графика
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect("equal", adjustable="box")  # Сохраняем пропорции
    plt.show()


def main() -> None:
    draw_shapes_and_add_colorful_legend(Circle(), Square())


if __name__ == "__main__":
    main()
