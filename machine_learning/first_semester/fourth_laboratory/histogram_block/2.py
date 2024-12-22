"""
2. Как отобразить значение каждого столбца на гистограмме с помощью Matplotlib?
"""
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from random import randint, choice
import string


@dataclass
class Column:
    data: int = field(default_factory=lambda: randint(0, 100))
    name: str = field(default_factory=lambda: f"{choice(string.ascii_uppercase)}")


def draw_histogram_and_show_value_of_each_column(*args: Column) -> None:
    names = [column.name for column in args]
    values = [column.data for column in args]

    bars = plt.barh(names, values)

    for bar in bars:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            str(bar.get_width()),
            va='center', ha='left'
        )

    plt.show()


def main() -> None:
    draw_histogram_and_show_value_of_each_column(
        Column(),
        Column(),
        Column(),
        Column()
    )


if __name__ == '__main__':
    main()
