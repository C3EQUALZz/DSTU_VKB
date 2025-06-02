"""
Вариант 12. Написать и протестировать функцию, которая находит в массиве минимальный по модулю элемент и заменяет
им все элементы с нечетными номерами.
"""

from typing import List


def replace_min_abs(arr: List[int]) -> List[int]:
    """
    Находит в массиве минимальный по модулю элемент и заменяет им все элементы с нечетными номерами (начиная с 1, индексы 0, 2, 4...).

    Аргументы:
        arr (List[int]): Исходный массив.

    Возвращает:
        List[int]: Модифицированный массив.
    """
    if not arr:
        return arr

    min_abs: int = min(arr, key=abs)
    for i in range(0, len(arr), 2):  # Не́четные номера → четные индексы
        arr[i] = min_abs
    return arr


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    try:
        user_input: List[int] = list(map(int, input("Введите элементы массива через пробел: ").split()))
        print("Исходный массив:", user_input)
        result: List[int] = replace_min_abs(user_input.copy())  # Не изменяем оригинальный массив
        print("Измененный массив:", result)
    except ValueError:
        print("Ошибка: Введите корректные целые числа.")


if __name__ == "__main__":
    main()