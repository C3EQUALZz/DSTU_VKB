"""
Задание 2. Найти теоретический материал, разобрать, составить блок-схему и реализовать сортировку слиянием на одномерном массиве.
"""

import sys

from algorithms_and_data_structures.second_laboratory.second_question.merge import \
    merge_sort


def main() -> None:
    while True:
        data = input("Введите данные для списка сортировки слиянием: ").split()

        if not all(x.isdigit() or x[1:].isdigit() for x in data):
            print("Вы ввели не цифры", file=sys.stderr)
            continue

        print(merge_sort([int(x) for x in data]))


if __name__ == "__main__":
    main()
