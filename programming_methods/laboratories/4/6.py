"""
Задача №3555. 10E: Pink Floyd

Группа Pink Floyd собирается отправиться в новый концертный тур по всему миру.
По предыдущему опыту группа знает, что солист Роджер Уотерс постоянно нервничает при перелетах.
На некоторых маршрутах он теряет вес от волнения, а на других — много ест и набирает вес.

Известно, что чем больше весит Роджер, тем лучше выступает группа, поэтому требуется спланировать перелеты так,
чтобы вес Роджера на каждом концерте был максимально возможным.

Группа должна посещать города в том же порядке, в котором она дает концерты.
При этом между концертами группа может посещать промежуточные города.

Входные данные

Первая строка входного файла содержит три натуральных числа n, m и k — количество городов в мире, количество рейсов и
количество концертов, которые должна дать группа соответственно (n≤100, m≤10000, 2≤k≤10000).
Города пронумерованы числами от 1 до n.

Следующие m строк содержат описание рейсов, по одному на строке.
Рейс номер i описывается тремя числами bi, ei и wi — номер начального и конечного города рейса и предполагаемое
изменение веса Роджера в миллиграммах (1≤bi,ei≤n, −100000≤wi≤100000).

Последняя строка содержит числа a1,a2,...,ak — номера городов, в которых проводятся концерты (ai≠ai+1).
В начале концертного тура группа находится в городе a1.

Гарантируется, что группа может дать все концерты.

Выходные данные

Первая строка выходного файла должна содержать число l — количество рейсов, которые должна сделать группа.
Вторая строка должна содержать l чисел — номера используемых рейсов.

Если существует такая последовательность маршрутов между концертами, что Роджер будет набирать вес неограниченно,
то первая строка выходного файла должна содержать строку „infinitely kind“.
"""
import sys
from dataclasses import dataclass
from typing import List, Tuple

INF = sys.maxsize // 2


@dataclass(frozen=True)
class Flight:
    start: int
    end: int
    weight_change: int
    index: int


def find_path_between_concerts(
        n: int,
        c: int,
        flights: List[Flight],
        concerts: List[int]
) -> Tuple[int, List[int]]:
    """
    Функция для нахождения маршрутов между концертами, минимизируя потерю веса.
    :param n: Количество городов
    :param c: Количество концертов
    :param flights: Список рейсов (класс Flight)
    :param concerts: Список городов, в которых будут проводиться концерты
    :return: Количество рейсов и список индексов рейсов
    """
    matrix = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    parents = [[0 for _ in range(n)] for _ in range(n)]

    for flight in flights:
        matrix[flight.start][flight.end] = -flight.weight_change
        parents[flight.start][flight.end] = flight.index

    # Алгоритм Флойда-Уоршелла для нахождения кратчайших путей
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    parents[i][j] = parents[i][k]

    # Проверка на отрицательные циклы
    for i in range(c):
        if matrix[concerts[i]][concerts[i]] < 0:
            return -1, []

    # Строим маршрут между концертами
    path = []
    for i in range(c - 1):
        v = concerts[i]
        while v != concerts[i + 1]:
            path.append(parents[v][concerts[i + 1]])
            v = flights[parents[v][concerts[i + 1]]].end
            if len(path) > 10000000:
                return -1, []

    return len(path), [p + 1 for p in path]


def main() -> None:
    n, m, c = map(int, input().split())
    flights: List[Flight] = []

    for i in range(m):
        vertex1, vertex2, w = map(int, input().split())
        vertex1 -= 1  # Приводим города к индексации с нуля
        vertex2 -= 1
        flights.append(Flight(vertex1, vertex2, w, i))

    concerts = [i - 1 for i in map(int, input().split())]

    # Получаем путь между концертами
    result, path = find_path_between_concerts(n, c, flights, concerts)

    if result == -1:
        print("infinitely kind")
    else:
        print(result)
        print(" ".join(map(str, path)))


if __name__ == "__main__":
    main()
