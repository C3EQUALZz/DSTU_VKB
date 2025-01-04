"""
Задача №112527. Реклама(3)

Фирма NNN решила транслировать свой рекламный ролик в супермаркете XXX.
Однако денег, запланированных на рекламную кампанию, хватило лишь на две трансляции ролика в течение одного рабочего дня.
И при этом обязательно транслировать ровно два рекламных ролика в день.

Фирма собрала информацию о количестве покупателей в каждый момент некоторого дня.
Менеджер по рекламе предположил, что и на следующий день покупатели будут приходить и уходить ровно в те же моменты времени.

Помогите ему определить моменты времени, когда нужно включить трансляцию рекламных роликов, чтобы как можно большее количество покупателей прослушало ролик.

Ролик длится ровно одну единицу времени.
Для каждого момента времени известно количество покупателей, находящихся в магазине в этот момент.
Между концом первой рекламы и началом следующей должна пройти как минимум К-1 единица времени.
"""
from itertools import combinations
from typing import List, Tuple


def get_max_indices(times: List[int]) -> Tuple[List[int], int]:
    """Возвращает индексы максимальных значений в списке."""
    max_value = max(times)
    return [i for i, value in enumerate(times) if value == max_value], max_value


def find_best_broadcast(times: List[int], k: int) -> int:
    """Находит наилучшие моменты для трансляции рекламы."""
    max_indices, max_1 = get_max_indices(times)

    # Проверяем, можно ли транслировать два ролика в максимальные моменты
    for i, j in combinations(max_indices, 2):
        if abs(i - j) > k - 1:
            return max_1 * 2

    # Если не удалось, ищем второй максимальный момент
    max_2 = max((times[i] for ind in max_indices for i in range(len(times))
                 if i != ind and abs(ind - i) > k - 1), default=0)

    if max_2 > 0:
        return max_1 + max_2

    # Если не нашли подходящие моменты, ищем альтернативный вариант
    max_sum = 0
    n = len(times)
    for i in range(n - k):
        edge = i + k
        if edge < n:
            j = max(times[edge:n])
            s = times[i] + j
            max_sum = max(max_sum, s)

    return max_sum


def main() -> None:
    n, k = map(int, input().split())
    times = list(map(int, input().split()))
    result = find_best_broadcast(times, k)
    print(result)


if __name__ == "__main__":
    main()
