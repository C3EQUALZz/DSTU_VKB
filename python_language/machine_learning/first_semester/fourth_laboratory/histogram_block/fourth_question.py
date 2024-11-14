"""
4. Как аннотировать столбцы в сгруппированном столбчатом графике на Python?
"""
from dataclasses import dataclass, field
from random import randint
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Column:
    name: str
    values: list[int] = field(default_factory=lambda: [randint(0, 100) for _ in range(2)])


@dataclass
class GroupedColumns:
    group_name: str
    columns: list[Column] = field(default_factory=list)


def draw_grouped_histogram_and_annotate_each_column(*args: GroupedColumns) -> None:
    # Проверка, что все группы имеют одинаковое количество колонок
    num_categories = len(args[0].columns)

    # Создание данных из переданных аргументов
    categories = [column.name for column in args[0].columns]
    fig, ax = plt.subplots()

    # Параметры графика
    bar_width = 0.8 / len(args)  # ширина столбцов зависит от количества групп
    index = np.arange(num_categories)

    # Построение сгруппированных столбцов
    for i, group in enumerate(args):
        values = [column.values[0] for column in group.columns]
        bars = ax.bar(index + i * bar_width, values, bar_width, label=group.group_name)

        # Аннотирование столбцов
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # смещение аннотации
                textcoords="offset points",
                ha='center', va='bottom'
            )

    ax.set_xticks(index + bar_width * (len(args) - 1) / 2)
    ax.set_xticklabels(categories)
    ax.legend()

    plt.show()


def main() -> None:
    draw_grouped_histogram_and_annotate_each_column(
        GroupedColumns(
            group_name="Group 1",
            columns=[
                Column(name="Category A"),
                Column(name="Category B"),
                Column(name="Category C")
            ]
        ),
        GroupedColumns(
            group_name="Group 2",
            columns=[
                Column(name="Category A"),
                Column(name="Category B"),
                Column(name="Category C")
            ]
        )
    )


if __name__ == '__main__':
    main()
