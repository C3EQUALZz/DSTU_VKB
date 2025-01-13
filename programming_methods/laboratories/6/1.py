"""
Задача №1361. Продажа билетов

В новых элитных электричках каждому пассажиру положено сидячее место.
Естественно, количество сидячих мест ограничено и на всех их может не хватить.
Маршрут электрички проходит через N+1 станция, занумерованные от 0 до N.
Когда человек хочет купить билет, он называет два числа x и y – номера станций, откуда и куда он хочет ехать.
При наличии хотя бы одного сидячего места на этом участке на момент покупки ему продается билет,
иначе выдается сообщение «билетов нет» и билет не продается.
Ваша задача – написать программу, обслуживающую такого рода запросы в порядке их прихода.

Входные данные

В первой строке содержаться три числа N – количество станций (1 ≤ N ≤ 200 000),
K – количество мест в электричке (1 ≤ K ≤ 1000) и M – количество запросов (1 ≤ M ≤ 100 000).
В следующих M строках описаны запросы, каждый из которых состоит из двух чисел x и y (0 ≤ x < y <= N).

Выходные данные

На каждый запрос ваша программа должна выдавать результат в виде числа 0 если билет не продается
и 1 если билет был продан. Каждый результат должен быть на отдельной строке.

НЕ ПРОХОДИТ ПО СКОРОСТИ ИЗ-ЗА PYTHON.
"""
from collections import deque
from typing import cast, Tuple, List, Iterable, Sequence


def is_available(
        segments: Sequence[int],
        start: int,
        end: int,
        k: int
) -> bool:
    """Проверяет, есть ли хотя бы одно свободное место на участке [x, y)."""
    return all(segments[i] < k for i in range(start, end))


def process_requests(
        count_of_stations: int,
        count_of_seats: int,
        requests: Iterable[Tuple[int, int]]
) -> Iterable[int]:
    """Обрабатывает все запросы на продажу билетов."""
    segments: List[int] = [0] * (count_of_stations + 1)  # Инициализируем массив мест
    results: deque[int] = deque()

    for start_station, end_station in requests:
        if is_available(segments, start_station, end_station, count_of_seats):
            # Если есть свободное место, продаем билет и увеличиваем занятые места
            for i in range(start_station, end_station):
                segments[i] += 1
            results.append(1)
        else:
            results.append(0)

    return results


def main() -> None:
    n, k, m = map(int, input().split())
    requests: List[Tuple[int, int]] = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(m)])

    results = process_requests(n, k, requests)
    print(*results, sep='\n')


if __name__ == "__main__":
    main()
