"""
Написать и протестировать функцию, вычисляющую x ** (1/3), используя итерационную формулу
"""


def cube_root(x: float) -> float:
    """
    Вычисляет кубический корень из x с помощью итерационной формулы:
    y_{i+1} = y_i + (1/3)(y_i^4 / x - y_i)

    Аргументы:
        x (float): Значение, для которого вычисляется корень. Должно удовлетворять 0 < |x| < 2.

    Возвращает:
        float: Приближенное значение кубического корня.

    Вызывает:
        ValueError: Если |x| ≥ 2 или x == 0.
    """
    if abs(x) >= 2 or x == 0:
        raise ValueError("x должен удовлетворять условию 0 < |x| < 2")

    y_prev: float = x

    while True:
        y_next: float = y_prev + (1/3) * (y_prev**4 / x - y_prev)

        if abs(y_next - y_prev) < 2e-6:
            break

        y_prev: float = y_next

    return y_next


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    try:
        x = float(input("Введите x (0 < |x| < 2): "))
        result: float = cube_root(x)
        print(f"Кубический корень из {x}: {result:.10f}")
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()