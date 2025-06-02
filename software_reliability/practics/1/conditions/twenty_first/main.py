"""
Вариант 21. Написать и протестировать функцию для нахождения в прямоугольной матрице номера строки,
имеющей максимальную сумму элементов.
"""
from typing import List


def max_row_sum_index(matrix: List[List[int]]) -> int:
    """
    Находит индекс строки матрицы с максимальной суммой элементов.

    Аргументы:
        matrix (List[List[int]]): Прямоугольная матрица.

    Возвращает:
        int: Индекс строки с максимальной суммой элементов.

    Вызывает:
        TypeError: Если матрица не является списком списков.
        ValueError: Если матрица пустая, содержит пустые строки или не прямоугольна.
    """
    if not isinstance(matrix, list):
        raise TypeError("Матрица должна быть списком.")

    if not matrix:
        raise ValueError("Матрица пустая.")

    # Проверяем, что все строки — списки и не пустые
    if not all(isinstance(row, list) and row for row in matrix):
        raise ValueError("Матрица содержит пустые строки.")

    # Проверяем, что матрица прямоугольная
    col_count: int = len(matrix[0])
    if not all(len(row) == col_count for row in matrix):
        raise ValueError("Матрица должна быть прямоугольной.")

    max_sum: int = sum(matrix[0])
    max_index: int = 0

    for i, row in enumerate(matrix):
        current_sum: int = sum(row)
        if current_sum > max_sum:
            max_sum: int = current_sum
            max_index: int = i

    return max_index


def main() -> None:
    """
    Основная функция, запрашивающая ввод матрицы и выводящая результат.
    """
    try:
        rows: int = int(input("Введите количество строк матрицы: "))
        cols: int = int(input("Введите количество столбцов матрицы: "))

        if rows <= 0 or cols <= 0:
            raise ValueError("Количество строк и столбцов должно быть положительным.")

        matrix: List[List[int]] = []
        for i in range(rows):
            row: List[int] = list(map(int, input(f"Введите {cols} чисел для строки {i + 1} через пробел: ").split()))
            if len(row) != cols:
                raise ValueError(f"Количество элементов в строке {i + 1} должно быть равно {cols}.")
            matrix.append(row)

        result: int = max_row_sum_index(matrix)
        print(f"Строка с максимальной суммой: {result}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()