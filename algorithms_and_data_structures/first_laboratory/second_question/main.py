"""
Задание 2. С помощью библиотеки time сравнить время выполнения каждой сортировки.
"""

from functools import wraps
from random import randint
from time import perf_counter_ns
from typing import Callable, Final, MutableSequence, Tuple

from algorithms_and_data_structures.core.types import CT
from algorithms_and_data_structures.first_laboratory.first_question.bubble import \
    bubble_sort
from algorithms_and_data_structures.first_laboratory.first_question.insertion import \
    insertion_sort
from algorithms_and_data_structures.first_laboratory.first_question.selection import \
    selection_sort

SortFunction = Callable[[MutableSequence[CT]], MutableSequence[CT]]


def work_time(func: SortFunction) -> SortFunction:
    """
    Декоратор, который измеряет время выполнения функции.
    Написан для сравнения по времени выполнения сортировок.
    :param func: Функция сортировки.
    :returns: Возвращает исходную функцию, выводя при этом в консоль время выполнения.
    """

    @wraps(func)
    def wrapped(*args: MutableSequence[CT]) -> MutableSequence[CT]:
        start = perf_counter_ns()
        res = func(*args)
        print(
            f"Сортировка {func.__name__}.\n"
            f"Количество элементов - {len(args[0])}.\n"
            f"Время выполнение: {perf_counter_ns() - start} ns\n"
        )
        return res

    return wrapped


ALGORITHMS: Final[Tuple[SortFunction, ...]] = tuple(
    map(work_time, (selection_sort, insertion_sort, bubble_sort))
)


def main() -> None:
    for len_of_array in (10, 100, 1_000_000, 10_000_000):
        data = [randint(1, 10000000000) for _ in range(len_of_array)]
        for algorithm in ALGORITHMS:
            algorithm(data.copy())


if __name__ == "__main__":
    main()
