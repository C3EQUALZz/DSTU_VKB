"""
Задача №364. Заполнение диагоналями

Даны числа n и m. Создайте массив A[n][m] и заполните его, как показано на примере.
"""
from typing import List


def fill_matrix(n: int, m: int) -> List[List[int]]:
    """
    Заполняет матрицу размером n на m по диагоналям.

    Количество диагоналей в матрице высчитывается по формуле n + m - 1. Как все-таки заполняется?
    Тут надо в зависимости от конкретного индекса диагонали высчитывать начальный индекс столбца и строки.

    Если индекс диагонали меньше количества столбцов в матрице, это означает, что мы находимся в верхней части матрицы,
    и начальная позиция будет в первой строке (start_row = 0) и в столбце index_of_diagonal.

    Если k больше или равен m, это означает, что мы достигли правого края матрицы, и начальная позиция будет в последнем
    столбце (start_col = m - 1) и в строке, которая определяется как k - m + 1.

    Дальше в цикле while идет заполнение диагонали.
    Главная сложность задачи - это найти правильное условие стартовых индексов диагонали.

    :param n: Количество строк.
    :param m: Количество столбцов.
    """
    matrix: List[List[int]] = [[0 for _ in range(m)] for _ in range(n)]
    count: int = 0

    for index_of_diagonal in range(n + m - 1):
        start_col: int
        start_row: int

        if index_of_diagonal < m:
            start_col = index_of_diagonal
            start_row = 0
        else:
            start_col = m - 1
            start_row = index_of_diagonal - m + 1

        while start_col >= 0 and start_row < n:
            matrix[start_row][start_col] = count
            count += 1
            start_col -= 1
            start_row += 1

    return matrix


def main() -> None:
    n, m = map(int, input().strip().split())
    matrix = fill_matrix(n, m)

    for row in matrix:
        print(' '.join(f'{num:3d}' for num in row))


if __name__ == "__main__":
    main()
