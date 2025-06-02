"""
Вариант 16. Написать и протестировать функцию, подсчитывающую количество положительных элементов в массиве.
"""

from typing import Iterable, List


def count_positive(arr: Iterable[int]) -> int:
    """
    Подсчитывает количество положительных элементов в массиве.

    Аргументы:
        arr (List[int]): Массив целых чисел.

    Возвращает:
        int: Количество положительных элементов (строго больше 0).
    """
    return sum(1 for x in arr if x > 0)


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    try:
        user_input: str = input("Введите элементы массива через пробел: ")
        arr: List[int] = list(map(int, user_input.split()))
        result: int = count_positive(arr)
        print(f"Количество положительных элементов: {result}")
    except ValueError:
        print("Ошибка: Введите корректные целые числа.")


if __name__ == "__main__":
    main()
