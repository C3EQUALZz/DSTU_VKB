"""
Даны две квадратные матрицы.
Напечатать ту из них, которая имеет минимальный «след», т. е. сумму элементов главной диагонали.
Использовать функцию для нахождения следа матрицы и функцию печати матрицы.
"""

from typing import List, Iterable


def trace(matrix: List[List[int]]) -> int:
    """
    Вычисляет след матрицы — сумму элементов главной диагонали.

    Аргументы:
        matrix (List[List[int]]): Квадратная матрица.

    Возвращает:
        int: Сумма элементов главной диагонали.
    """
    return sum(matrix[i][i] for i in range(len(matrix)))


def print_matrix(matrix: Iterable[Iterable[int]]) -> None:
    """
    Печатает матрицу в удобочитаемом виде.

    Аргументы:
        matrix (List[List[int]]): Матрица для печати.
    """
    for row in matrix:
        print(" ".join(map(str, row)))


def read_matrix(n: int) -> List[List[int]]:
    """
    Считывает матрицу размером n x n из пользовательского ввода.

    Аргументы:
        n (int): Размерность матрицы.

    Возвращает:
        List[List[int]]: Считанная матрица.
    """
    matrix: List[List[int]] = []
    for _ in range(n):
        row: List[int] = list(map(int, input().split()))
        matrix.append(row)
    return matrix


def main() -> None:
    """
    Основная функция программы.
    Запрашивает у пользователя ввод двух квадратных матриц,
    вычисляет их следы и печатает матрицу с минимальным следом.
    """
    try:
        n = int(input("Введите размерность квадратных матриц: "))

        print("Введите первую матрицу:")
        matrix_a = read_matrix(n)

        print("Введите вторую матрицу:")
        matrix_b = read_matrix(n)

        trace_a = trace(matrix_a)
        trace_b = trace(matrix_b)

        print("Матрица с минимальным следом:")

        if trace_a <= trace_b:
            print_matrix(matrix_a)
        else:
            print_matrix(matrix_b)

    except ValueError:
        print("Ошибка: Введите корректные числовые значения.")
    except IndexError:
        print("Ошибка: Некорректный формат ввода матрицы.")


if __name__ == "__main__":
    main()
