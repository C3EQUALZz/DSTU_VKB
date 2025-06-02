"""
По заданным значениям X[20], Y[20] вычислить (там формула)
"""
from typing import List


def calculate_u(x: List[float], y: List[float]) -> float:
    """
    Вычисляет значение u по заданным массивам X и Y согласно варианту.

    Параметры:
        x (list[float]): Массив из 20 элементов
        y (list[float]): Массив из 20 элементов

    Возвращает:
        float: Результат вычисления u

    Исключения:
        ValueError: Если размеры массивов не равны 20
    """
    if len(x) != 20 or len(y) != 20:
        raise ValueError("Оба массива должны содержать ровно 20 элементов")

    # Вычисляем сумму произведений x_i * y_i для i=0..14 (что соответствует i=1..15 в условии)
    s: int = sum(x[i] * y[i] for i in range(15))

    if s > 0:
        return sum(val ** 2 for val in x)
    return sum(y[i] ** 2 for i in range(9, 19))


def main() -> None:
    """Основная функция для ввода данных и вывода результата"""
    print("Вычисление значения u по заданным массивам X и Y")
    print("------------------------------------------------")
    print("Введите 20 вещественных чисел для массива X:")

    x: List[float] = []
    for i in range(20):
        while True:
            try:
                val: float = float(input(f"X[{i + 1}]: "))
                x.append(val)
                break
            except ValueError:
                print("Ошибка: Введите число!")

    print("\nВведите 20 вещественных чисел для массива Y:")

    y: List[float] = []
    for i in range(20):
        while True:
            try:
                val: float = float(input(f"Y[{i + 1}]: "))
                y.append(val)
                break
            except ValueError:
                print("Ошибка: Введите число!")

    try:
        result: float = calculate_u(x, y)
        print(f"\nРезультат вычисления u = {result:.6f}")
    except ValueError as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()