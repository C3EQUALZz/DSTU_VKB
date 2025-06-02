"""
Вариант 20. Написать и протестировать функцию для вычисления площади треугольника, заданного координатами вершин.
"""

from typing import Tuple, cast


def area_triangle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    """
    Вычисляет площадь треугольника, заданного координатами своих вершин.

    Аргументы:
        a (Tuple[float, float]): Координаты первой точки (x, y).
        b (Tuple[float, float]): Координаты второй точки (x, y).
        c (Tuple[float, float]): Координаты третьей точки (x, y).

    Возвращает:
        float: Площадь треугольника.
    """
    # Используем формулу площади через векторное произведение
    ax, ay = a
    bx, by = b
    cx, cy = c

    # Векторы AB и AC
    ab_x, ab_y = bx - ax, by - ay
    ac_x, ac_y = cx - ax, cy - ay

    # Векторное произведение AB × AC
    cross_product = ab_x * ac_y - ac_x * ab_y

    # Площадь равна половине модуля векторного произведения
    return abs(cross_product) / 2


def main() -> None:
    """
    Основная функция, запрашивающая координаты вершин треугольника
    и выводящая площадь треугольника.
    """
    try:
        print("Введите координаты трех точек, задающих треугольник.")
        print("Формат ввода: x y")

        a: tuple[float, float] = cast(tuple[float, float], tuple(map(float, input("Координаты точки A (x y): ").split())))
        b: tuple[float, float] = cast(tuple[float, float], tuple(map(float, input("Координаты точки B (x y): ").split())))
        c: tuple[float, float] = cast(tuple[float, float], tuple(map(float, input("Координаты точки C (x y): ").split())))

        if len(a) != 2 or len(b) != 2 or len(c) != 2:
            raise ValueError("Каждая точка должна содержать ровно 2 числа.")

        area: float = area_triangle(a, b, c)
        print(f"Площадь треугольника: {area:.6f}")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
