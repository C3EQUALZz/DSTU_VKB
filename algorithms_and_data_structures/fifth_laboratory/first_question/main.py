import sys

from algorithms_and_data_structures.fifth_laboratory.first_question.mine_implementation import \
    heap_sort as heap_sort_mine
from algorithms_and_data_structures.fifth_laboratory.first_question.using_heapq import \
    heap_sort as heap_sort_using_heapq

CHOICES = {
    "1": heap_sort_mine,
    "2": heap_sort_using_heapq,
}


def main() -> None:
    while True:
        user_data = input(
            "Введите каким способом сделать сортировку кучей:"
            "\n(1) - моя реализация"
            "\n(2) - использование heapq"
        )

        if user_data not in CHOICES:
            print("Неправильный выбор", file=sys.stderr)
            continue

        CHOICES[user_data]([int(x) for x in input("Введите данные для сортировки через пробел: ").strip().split()])


if __name__ == '__main__':
    main()
