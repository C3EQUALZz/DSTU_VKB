# Найти симметричные пары в массиве

from collections import Counter, deque
from typing import Sequence


def find_symmetric_pairs(pairs: list[list[int]]) -> Sequence[list[int]]:
    freq: Counter[tuple] = Counter(map(tuple, pairs))
    unique_pairs = set(map(tuple, pairs))

    result: deque[list[int]] = deque()
    # Проверяем каждую пару на наличие симметричной

    for pair in pairs:
        p = tuple(pair)
        x, y = p
        reversed_pair = (y, x)
        if reversed_pair in unique_pairs:
            # Для пар с одинаковыми элементами проверяем частоту
            if x != y or (x == y and freq[p] >= 2):
                result.append(list(p))
    return result


def main() -> None:
    pairs = [[1, 2], [2, 1], [3, 4], [4, 5], [5, 4], [3, 3], [3, 3]]
    print(find_symmetric_pairs(pairs))
    # Вывод: [[1, 2], [2, 1], [4, 5], [5, 4], [3, 3], [3, 3]]


if __name__ == '__main__':
    main()
