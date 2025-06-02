"""
Cоставить и протестировать функцию для вычисления
"""

import math


def calculate_series(x: float, n: int, m: int) -> float:
    """
    Вычисляет сумму ряда f(x, n, m) = Σ (x^(2i)/(2i!)) для i от n до m.

    Аргументы:
        x (float): Базовое значение для возведения в степень.
        n (int): Начальный индекс суммирования.
        m (int): Конечный индекс суммирования.

    Возвращает:
        float: Значение суммы ряда.
    """
    if n > m:
        return 0.0

    total: float = 0.0
    for i in range(n, m + 1):
        exponent: int = 2 * i
        factorial: float = math.factorial(exponent)
        term: float = (x ** exponent) / factorial
        total += term

    return total


def main() -> None:
    """
    Основная функция, запрашивающая данные у пользователя и выводящая результат.
    """
    try:
        x = float(input("Введите значение x: "))
        n = int(input("Введите начальный индекс n: "))
        m = int(input("Введите конечный индекс m: "))

        result = calculate_series(x, n, m)
        print(f"Сумма ряда: {result:.10f}")

    except ValueError:
        print("Ошибка: Введите корректные числовые значения.")
    except OverflowError:
        print("Ошибка: Число слишком велико для обработки.")


if __name__ == "__main__":
    main()
