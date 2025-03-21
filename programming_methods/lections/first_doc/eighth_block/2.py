# Найти, если массив является подмножеством другого массива
from typing import Iterable


def check_intersection_of_arrays(first: Iterable[int], second: Iterable[int]) -> bool:
    return bool(set(first).intersection(second))


def main() -> None:
    first = [1, 2, 3]
    second = [1, 2, 3]
    print(check_intersection_of_arrays(first, second))


if __name__ == '__main__':
    main()
