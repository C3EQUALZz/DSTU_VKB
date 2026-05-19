"""Оригинальная реализация classify_triangle из задания.

Содержит ряд дефектов:
    1. Нет проверки неравенства треугольника (a+b>c, a+c>b, b+c>a).
       На вырожденном или несуществующем треугольнике возвращает
       «Равнобедренный» / «Разносторонний» вместо «InvalidInput».
       Классический пример из задания: classify_triangle(7, 7, 14)
       вернёт «Равнобедренный», хотя 7 + 7 = 14 — это вырожденный
       треугольник (точки лежат на одной прямой).
    2. Docstring обещает строки на английском
       («Equilateral», «Isosceles», «Scalene», «InvalidInput»),
       а фактически возвращаются русские строки. Это рассогласование
       спецификации и реализации.
    3. isinstance(side, int) пропускает bool: classify_triangle(True, True, True)
       будет принят как валидный «Равносторонний».

Модуль оставлен для демонстрации в README и в тестах-«пугалках».
Использовать в продакшене не следует — обращайтесь к
``second_laboratory.triangle.classify_triangle``.
"""

from __future__ import annotations


def classify_triangle(a, b, c):
    """
    Классифицирует треугольник по трём сторонам.

    Возвращает:
        - "Equilateral"  : равносторонний
        - "Isosceles"    : равнобедренный (но не равносторонний)
        - "Scalene"      : разносторонний
        - "InvalidInput" : недопустимый ввод (<= 0 или не int)
    """
    # Проверка типа и положительности
    if not all(isinstance(side, int) for side in (a, b, c)):
        return "InvalidInput"
    if any(side <= 0 for side in (a, b, c)):
        return "InvalidInput"
    # Определение типа
    if a == b == c:
        return "Равносторонний"
    elif a == b or b == c or a == c:
        return "Равнобедренный"
    else:
        return "Разносторонний"


if __name__ == "__main__":
    print(classify_triangle(7, 7, 14))
