"""
Задача №364. Заполнение диагоналями

Даны числа n и m. Создайте массив A[n][m] и заполните его, как показано на примере.

0  1  3  6 10 14 18 22 26 30
2  4  7 11 15 19 23 27 31 34
5  8 12 16 20 24 28 32 35 37
9 13 17 21 25 29 33 36 38 39
"""
from typing import List


def fill_matrix(n: int, m: int) -> List[List[int]]:
    """Заполняет матрицу размером n на m по диагоналям."""
    matrix = [[0 for _ in range(m)] for _ in range(n)]
    count = 0

    for k in range(n + m - 1):
        if k < m:
            start_col = k
            start_row = 0
        else:
            start_col = m - 1
            start_row = k - m + 1

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
