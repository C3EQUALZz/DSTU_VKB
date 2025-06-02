"""
Вариант 14. Написать и протестировать функцию, которая по заданному натуральному числу определяет количество цифр в нем и их сумму.
"""

from typing import Tuple, List


def count_digits_and_sum(n: int) -> Tuple[int, int]:
    """
    Определяет количество цифр в натуральном числе и их сумму.

    Аргументы:
        n (int): Натуральное число (n ≥ 1).

    Возвращает:
        Tuple[int, int]: Кортеж (количество_цифр, сумма_цифр).

    Вызывает:
        ValueError: Если n не является натуральным числом.
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("Входное значение должно быть натуральным числом (n ≥ 1).")

    s: str = str(n)
    digits: List[int] = [int(c) for c in s]
    return len(s), sum(digits)


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    try:
        num: int = int(input("Введите натуральное число: "))
        count, total = count_digits_and_sum(num)
        print(f"Количество цифр: {count}")
        print(f"Сумма цифр: {total}")
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
