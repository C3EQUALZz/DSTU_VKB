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
from itertools import combinations, product
from typing import List, Set, Iterable, Tuple


def find_best_broadcast(n: int, k: int, times: List[int]) -> int:
    """
    Нам нужно найти максимальное выгодное время для показа 2 реклам.
    Очевидно, что надо показывать, когда больше всего покупателей.

    Первый возможный вариант: два и более пришло максимальное количество людей.
    Если сопоставить всех их возможные комбинации, проверив, что разница по времени между ними k-1,
    то мы найдем максимальное количество людей. Напоминаю, что индексы - это время.

    Второй возможный вариант: ищем пред максимальное количество людей,
    проверяя на условие, что разница между максимальным и пред максимальным равно по времени k-1.

    Третий вариант: если не нашли комбинацию с максимумом, то нам нужно отталкиваться от других возможных пар.

    :param n: Количество моментов времени, когда нужно отследить покупателей.
    :param k: Время совершение покупки одним покупателем.
    :param times: Количество покупателей в определенные моменты.
    :returns: Количество просмотревших рекламу покупателей.
    """
    maximum_number_of_people: int = max(times)
    indexes_of_moments_when_maximum_number_of_people: Set[int] = {index for index, value in enumerate(times)
                                                                  if value == maximum_number_of_people}

    # Проверяем, можно ли транслировать два ролика в максимальные моменты
    for i, j in combinations(indexes_of_moments_when_maximum_number_of_people, 2):
        if abs(i - j) > k - 1:
            return maximum_number_of_people * 2

    # Если не удалось, ищем пред максимальный момент
    all_possible_pairs_with_a_maximum: Iterable[Tuple[int, int]] = product(
        indexes_of_moments_when_maximum_number_of_people,
        range(len(times))
    )

    pre_max_number_of_people: int = max(
        map(
            lambda index_pair: times[index_pair[1]],
            filter(
                lambda index_pair: index_pair[0] != index_pair[1] and abs(index_pair[0] - index_pair[1]) > k - 1,
                all_possible_pairs_with_a_maximum
            )
        ),
        default=0
    )

    if pre_max_number_of_people > 0:
        return maximum_number_of_people + pre_max_number_of_people

    # Если не нашли подходящие моменты, ищем альтернативный вариант
    max_viewers_sum: int = 0

    # Проходим по всем возможным начальным моментам времени для первой рекламы
    for start_time in range(n - k):
        # Вычисляем момент времени, когда может начаться вторая реклама
        second_ad_start_time: int = start_time + k
        if second_ad_start_time < n:
            # Суммируем количество покупателей в момент начала первой рекламы
            # и максимальное количество покупателей в момент времени после первой рекламы
            viewers_sum: int = times[start_time] + max(times[second_ad_start_time:n])
            max_viewers_sum = max(max_viewers_sum, viewers_sum)

    return max_viewers_sum


def main() -> None:
    n, k = map(int, input().split())
    times = list(map(int, input().split()))
    result = find_best_broadcast(n, k, times)
    print(result)


if __name__ == "__main__":
    main()
