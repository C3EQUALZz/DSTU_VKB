"""
Задан список с числами.
Напишите функцию, которая добавляет все элементы с четными индексами в новый список и возвращает его.

Тестовые данные:
- 1 2 3 4 5 6 7 8 9 10
"""
from typing import Any


def get_list_with_even_idx(lst: list[Any]) -> list[Any]:
    return [element for index, element in enumerate(lst) if index % 2 == 0]


def main():
    print(get_list_with_even_idx(input("Введите подряд элементы через пробел: ").split()))


if __name__ == '__main__':
    main()
