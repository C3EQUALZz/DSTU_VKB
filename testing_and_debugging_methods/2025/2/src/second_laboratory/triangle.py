"""Исправленная реализация classify_triangle.

Изменения по сравнению с оригиналом (см. ``legacy.py``):

1. Возвращаемые значения приведены к docstring контракту —
   английские строки: ``Equilateral`` / ``Isosceles`` / ``Scalene`` /
   ``InvalidInput``.
2. Явно отвергается ``bool`` (это подкласс ``int`` в Python,
   но не имеет смысла как длина стороны).
3. Добавлена проверка **неравенства треугольника**:
   для существования невырожденного треугольника необходимо
   ``a + b > c`` И ``a + c > b`` И ``b + c > a``.
   Вырожденный случай (равенство) также считается InvalidInput.
"""

from __future__ import annotations

from typing import Literal

TriangleKind = Literal["Equilateral", "Isosceles", "Scalene", "InvalidInput"]


def classify_triangle(a: int, b: int, c: int) -> TriangleKind:
    """
    Классифицирует треугольник по трём сторонам.

    Возвращает:
        - "Equilateral"  : равносторонний (все три стороны равны)
        - "Isosceles"    : равнобедренный (ровно две стороны равны)
        - "Scalene"      : разносторонний (все стороны разные)
        - "InvalidInput" : недопустимый ввод — не int, <= 0,
                           либо стороны не образуют треугольник
                           (нарушено неравенство треугольника).
    """
    # 1. Тип: только int, bool явно отвергаем
    for side in (a, b, c):
        if isinstance(side, bool) or not isinstance(side, int):
            return "InvalidInput"

    # 2. Положительность сторон
    if a <= 0 or b <= 0 or c <= 0:
        return "InvalidInput"

    # 3. Неравенство треугольника: сумма любых двух сторон больше третьей.
    #    Знак строго ">", иначе получаем вырожденный треугольник.
    if a + b <= c or a + c <= b or b + c <= a:
        return "InvalidInput"

    # 4. Определение типа
    if a == b == c:
        return "Equilateral"
    if a == b or b == c or a == c:
        return "Isosceles"
    return "Scalene"


if __name__ == "__main__":
    print(classify_triangle(7, 7, 14))   # InvalidInput (вырожденный)
    print(classify_triangle(3, 4, 5))    # Scalene
    print(classify_triangle(5, 5, 5))    # Equilateral
    print(classify_triangle(5, 5, 8))    # Isosceles
