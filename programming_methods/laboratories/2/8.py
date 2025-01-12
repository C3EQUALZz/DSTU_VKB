"""
Задача №672. Провода

Дано N отрезков провода длиной L1, L2, ..., LN сантиметров.
Требуется с помощью разрезания получить из них K равных отрезков как можно большей длины, выражающейся целым числом сантиметров.
Если нельзя получить K отрезков длиной даже 1 см, вывести 0.

Ограничения: 1 <= N <= 10 000, 1 <= K <= 10 000, 100 <= Li <= 10 000 000, все числа целые.

Входные данные

В первой строке находятся числа N и К. В следующих N строках - L1, L2, ..., LN, по одному числу в строке.

Выходные данные

Вывести одно число - полученную длину отрезков.
"""
from typing import List, Sequence


def max_segment_length(segments: Sequence[int], required_segments: int) -> int:
    """
    Здесь задача заключается на бинарный поиск.
    Из условия задачи нам известны ограничения справа и слева.

    В цикле мы считаем количество сегментов.
    Если их больше, чем требуется, то можем увеличить длину, в ином случае уменьшаем.

    Цикл заканчивается, когда left и right сойдутся.
    Если они - левая и правая граница - сошлись, то максимальное расстояние - это left - 1 (прошлая иттерация)

    :param segments: Отрезки провода.
    :param required_segments: Количество отрезков, которые требуются получить из условия задачи.

    :returns: Максимальная длина отрезков.
    """
    left: int = 1
    right: int = 10_000_001

    while left < right:
        mid: int = (left + right) // 2
        total_segments: int = sum(length // mid for length in segments)

        if total_segments >= required_segments:
            left = mid + 1
        else:
            right = mid

    return left - 1


def main() -> None:
    n, k = map(int, input().split())
    segments: List[int] = [int(input()) for _ in range(n)]

    result: int = max_segment_length(segments, k)
    print(result)


if __name__ == "__main__":
    main()
