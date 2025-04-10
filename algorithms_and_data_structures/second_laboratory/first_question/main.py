"""
Задание 1. В двумерном массиве все элементы по столбцам упорядочить с помощью алгоритмов Шелла (1 вариант) или Хоара
(2 вариант), в зависимости от порядкового номера по списку группы.
"""

import sys
from random import randint

from algorithms_and_data_structures.second_laboratory.first_question.quick import \
    quick_sort
from algorithms_and_data_structures.second_laboratory.first_question.shell import \
    shell_sort

algorithms = {"1": quick_sort, "2": shell_sort}


def main() -> None:
    while True:
        choice = input(
            "Введите какой алгоритм вы хотите?\n(1) - быстрая сортировка\n(2) - сортировка Шелла\n"
        )

        if choice not in algorithms:
            print("Вы выбрали неправильный вариант", file=sys.stderr)
            continue

        n, m = map(int, input("Введите два числа размерности матрицы: ").split())

        data = [[randint(-1000, 1000) for x in range(m)] for _ in range(n)]

        print(
            "Изначальная матрица: ",
            "\n".join(" ".join(map(str, x)) for x in data),
            sep="\n",
        )

        result_matrix = []

        for column in zip(*data):
            result_matrix.append(algorithms[choice](column))

        print(
            "Отсортированная по столбцам матрица: ",
            "\n".join(" ".join(map(str, x)) for x in zip(*result_matrix)),
            sep="\n",
        )


if __name__ == "__main__":
    main()
