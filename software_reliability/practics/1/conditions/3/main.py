"""
Написать и протестировать функцию, подсчитывающую количество минимальных элементов в каждой строке целочисленной матрицы.
"""

from collections import deque
from typing import Sequence


def count_min_in_rows(matrix: Sequence[Sequence[int]]) -> Sequence[int]:
    """
    Подсчитывает количество минимальных элементов в каждой строке матрицы.

    Параметры:
        matrix (Sequence[Sequence[int]]): Целочисленная матрица

    Возвращает:
        Sequence[int]: последовательность, где i-й элемент - количество минимальных элементов в i-й строке

    Исключения:
        ValueError: Если матрица пустая или содержит пустые строки
    """
    if not matrix:
        raise ValueError("Матрица пустая")

    if any(len(row) == 0 for row in matrix):
        raise ValueError("Матрица содержит пустые строки")

    result: deque[int] = deque()
    for row in matrix:
        min_val: int = min(row)
        count: int = sum(1 for element in row if element == min_val)
        result.append(count)

    return result


def main() -> None:
    """Основная функция для ввода матрицы и вывода результатов"""
    print("Подсчет количества минимальных элементов в каждой строке матрицы")
    print("-------------------------------------------------------------")

    # Ввод количества строк
    while True:
        try:
            rows = int(input("Введите количество строк матрицы: "))
            if rows <= 0:
                print("Ошибка: Количество строк должно быть положительным числом!")
                continue
            break
        except ValueError:
            print("Ошибка: Введите целое число!")

    matrix: list[list[int]] = []
    print("\nВведите строки матрицы (целые числа через пробел):")

    # Ввод каждой строки матрицы
    for i in range(rows):
        while True:
            try:
                row_input: str = input(f"Строка {i + 1}: ").strip()
                if not row_input:
                    print("Ошибка: Строка не может быть пустой!")
                    continue

                row: list[int] = list(map(int, row_input.split()))
                matrix.append(row)
                break
            except ValueError:
                print("Ошибка: Вводите только целые числа, разделенные пробелами!")

    # Обработка и вывод результатов
    try:
        results: Sequence[int] = count_min_in_rows(matrix)
        print("\nРезультаты:")
        for i, count in enumerate(results):
            print(f"Строка {i + 1}: {count} минимальных элементов")
    except ValueError as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()
