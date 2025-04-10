"""
Задание 1. Реализовать сортировку «пузырьком». Сортировку выбором и сортировку вставкой.
"""

import sys

from algorithms_and_data_structures.first_laboratory.first_question.bubble import \
    bubble_sort
from algorithms_and_data_structures.first_laboratory.first_question.insertion import \
    insertion_sort
from algorithms_and_data_structures.first_laboratory.first_question.selection import \
    selection_sort

questions = {
    "1": bubble_sort,
    "2": selection_sort,
    "3": insertion_sort,
}


def main() -> None:
    while True:
        question = input(
            "Выберите какую сортировку вы хотите?\n(1) - пузырек\n(2) - выбор\n(3) - вставка\n"
        )

        if question not in questions:
            print("Вы выбрали неправильный вариант", file=sys.stderr)
            continue

        data = [int(x) for x in input("Введите числа через пробел: ").strip().split()]

        print(questions[question](data))


if __name__ == "__main__":
    main()
