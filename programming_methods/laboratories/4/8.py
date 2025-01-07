"""
Задача №524. Рейсы во времени

Между N населенными пунктами совершаются пассажирские рейсы на машинах времени.

В момент времени 0 вы находитесь в пункте A. Вам дано расписание рейсов.
Требуется оказаться в пункте B как можно раньше (то есть в наименьший возможный момент времени).

При этом разрешается делать пересадки с одного рейса на другой.
Если вы прибываете в некоторый пункт в момент времени T, то вы можете уехать из него любым рейсом,
который отправляется из этого пункта в момент времени T или позднее (но не раньше).

Входные данные

В первой строке вводится число N – количество населенных пунктов (1≤N≤1000).
Вторая строка содержит два числа A и B – номера начального и конечного пунктов.
В третьей строке задается K – количество рейсов (0≤K≤1000).
Следующие K строк содержат описания рейсов, по одному на строке.
Каждое описание представляет собой четверку целых чисел.
Первое число каждой четверки задает номер пункта отправления, второе – время отправления, третье – пункт назначения,
четвертое – время прибытия. Номера пунктов – натуральные числа из диапазона от 1 до N.
Пункт назначения и пункт отправления могут совпадать.
Время измеряется в некоторых абсолютных единицах и задается целым числом, по модулю не превышающим 10^9.
Поскольку рейсы совершаются на машинах времени, то время прибытия может быть как больше времени отправления, так и меньше, или равным ему.

Гарантируется, что входные данные таковы, что добраться из пункта A в пункт B всегда можно.

Выходные данные

Выведите минимальное время, когда вы сможете оказаться в пункте B.
"""
import heapq
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class Flight:
    src: int
    dep_time: int
    dest: int
    arr_time: int


@dataclass
class Graph:
    adjacency_list: Dict[int, List[Tuple[int, int, int]]] = field(default_factory=lambda: defaultdict(list))

    def add_flight(self, flight: Flight) -> None:
        self.adjacency_list[flight.src].append((flight.dest, flight.dep_time, flight.arr_time))

    def get_neighbors(self, node: int) -> List[Tuple[int, int, int]]:
        return self.adjacency_list.get(node, [])


def min_time_to_destination(n: int, a: int, b: int, graph: Graph) -> int:
    min_time = [float('inf')] * (n + 1)
    min_time[a] = 0
    heap = [(0, a)]

    while heap:
        time, node = heapq.heappop(heap)
        if time > min_time[node]:
            continue
        for dest, dep_time, arr_time in graph.get_neighbors(node):
            if dep_time >= time and min_time[dest] > arr_time:
                min_time[dest] = arr_time
                heapq.heappush(heap, (arr_time, dest))

    return round(min_time[b])


def main() -> None:
    n = int(input())
    a, b = map(int, input().split())
    k = int(input())

    flights: List[Flight] = [Flight(*map(int, input().split())) for _ in range(k)]

    graph = Graph()
    for flight in flights:
        graph.add_flight(flight)

    result: int = min_time_to_destination(n, a, b, graph)
    print(result)


if __name__ == "__main__":
    main()
