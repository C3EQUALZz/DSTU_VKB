"""
Вариант 13. Написать и протестировать функцию, которая в прямоугольной матрице находит сумму элементов j-й строки.
"""

from typing import List


def sum_row(matrix: List[List[int]], j: int) -> int:
    """
    Возвращает сумму элементов j-й строки прямоугольной матрицы.

    Аргументы:
        matrix (List[List[int]]): Прямоугольная матрица.
        j (int): Индекс строки (начиная с 0).

    Возвращает:
        int: Сумма элементов строки.

    Вызывает:
        IndexError: Если индекс j выходит за границы матрицы.
    """
    if not matrix:
        raise ValueError("Матрица пуста.")

    if j < 0 or j >= len(matrix):
        raise IndexError("Индекс строки выходит за границы матрицы.")

    return sum(matrix[j])


def main() -> None:
    """
    Основная функция, запрашивающая ввод матрицы и индекса строки,
    затем выводящая сумму элементов указанной строки.
    """
    try:
        rows: int = int(input("Введите количество строк матрицы: "))
        cols: int = int(input("Введите количество столбцов матрицы: "))

        matrix: List[List[int]] = []
        for i in range(rows):
            row: List[int] = list(map(int, input(f"Введите {cols} чисел для строки {i + 1} через пробел: ").split()))
            if len(row) != cols:
                raise ValueError(f"Количество элементов в строке {i + 1} должно быть равно {cols}.")
            matrix.append(row)

        j: int = int(input("Введите индекс строки для суммирования (начиная с 0): "))
        result: int = sum_row(matrix, j)
        print(f"Сумма элементов строки {j}: {result}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except IndexError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
