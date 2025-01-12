"""
Задача №1790. НОП с восстановлением

Даны две последовательности, требуется найти и вывести их наибольшую общую подпоследовательность.

Входные данные

В первой строке входных данных содержится число N– длина первой последовательности (1 ≤ N ≤ 1000).
Во второй строке заданы члены первой последовательности (через пробел) – целые числа, не превосходящие 10000 по модулю.

В третьей строке записано число M– длина второй последовательности (1 ≤ M≤ 1000).
В четвертой строке задаются члены второй последовательности (через пробел) – целые числа, не превосходящие 10000 по модулю.

Выходные данные

Требуется вывести наибольшую общую подпоследовательность данных последовательностей, через пробел.
"""
from typing import List, Sequence
from itertools import product


def find_longest_common_subsequence(
        len_seq_a: int,
        sequence_a: Sequence[int],
        len_seq_b: int,
        sequence_b: Sequence[int]
) -> List[int]:
    """
    Находит наибольшую общую подпоследовательность двух последовательностей.

    Принимает длины двух последовательностей и сами последовательности в виде списков целых чисел.
    Создает двумерный массив `lcs_length_table`, где `lcs_length_table[i][j]` хранит длину наибольшей общей
    подпоследовательности для первых `i` элементов первой последовательности и первых `j` элементов
    второй последовательности.

    Заполняет таблицу, сравнивая элементы последовательностей:
    - Если элементы совпадают, увеличивает длину LCS на 1.
    - Если не совпадают, берет максимальное значение из предыдущих вычислений.
    Восстанавливает саму наибольшую общую подпоследовательность, проходя по таблице от конца к началу.
    Возвращает LCS в правильном порядке.
    """
    # Создаем таблицу для хранения длины LCS
    lcs_length_table: List[List[int]] = [[0] * (len_seq_b + 1) for _ in range(len_seq_a + 1)]

    # Заполняем таблицу
    for i, j in product(range(1, len_seq_a + 1), range(1, len_seq_b + 1)):
        if sequence_a[i - 1] == sequence_b[j - 1]:
            lcs_length_table[i][j] = lcs_length_table[i - 1][j - 1] + 1
        else:
            lcs_length_table[i][j] = max(lcs_length_table[i - 1][j], lcs_length_table[i][j - 1])

    # Восстанавливаем LCS
    longest_common_subseq: List[int] = []
    i: int = len_seq_a
    j: int = len_seq_b
    while i > 0 and j > 0:
        if sequence_a[i - 1] == sequence_b[j - 1]:
            longest_common_subseq.append(sequence_a[i - 1])
            i -= 1
            j -= 1
        elif lcs_length_table[i - 1][j] == lcs_length_table[i][j]:
            i -= 1
        else:
            j -= 1

    return longest_common_subseq[::-1]


def main() -> None:
    len_seq_a: int = int(input())
    sequence_a: List[int] = list(map(int, input().split()))
    len_seq_b: int = int(input())
    sequence_b: List[int] = list(map(int, input().split()))

    longest_common_subseq: List[int] = find_longest_common_subsequence(len_seq_a, sequence_a, len_seq_b, sequence_b)
    print(' '.join(map(str, longest_common_subseq)))


if __name__ == "__main__":
    main()
