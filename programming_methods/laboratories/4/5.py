"""
Задача №113213. Заправки-2

В стране N городов, некоторые из которых соединены между собой дорогами.
Для того, чтобы проехать по одной дороге, требуется один бак бензина.
Помимо этого у вас есть канистра для бензина, куда входит столько же топлива, сколько входит в бензобак.

В каждом городе бак бензина имеет разную стоимость. Вам требуется добраться из первого города в N-й, потратив как можно меньшее денег.

В каждом городе можно заправить бак, заправить бак и канистру или же перелить бензин из канистры в бак.
Это позволяет экономить деньги, покупая бензин в тех городах, где он стоит дешевле, но канистры хватает только на одну заправку бака!

Входные данные

В первой строке вводится число N(1≤N≤100), в следующей строке идет N чисел, i-е из которых задает стоимость бензина в
i-м городе (всё это целые числа из диапазона от 0 до 100).
Затем идет число M– количество дорог в стране, далее идет описание самих дорог.
Каждая дорога задается двумя числами – номерами городов, которые она соединяет.
Все дороги двухсторонние (то есть по ним можно ездить как в одну, так и в другую сторону),
между двумя городами всегда существует не более одной дороги, не существует дорог, ведущих из города в себя.

Выходные данные

Требуется вывести одно число – суммарную стоимость маршрута или -1, если добраться невозможно.
"""
from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from heapq import heappop, heappush
from typing import List, Tuple, Dict, Set, cast


@dataclass
@total_ordering
class State:
    """
    Класс, представляющий состояние во время поиска минимальной стоимости топлива.

    Атрибуты:
    cost (int): Общая стоимость топлива, потраченная до текущего состояния.
    city (int): Номер текущего города.
    tank (int): Количество топлива в баке (0 или 1).
    canister (int): Количество топлива в канистре (0 или 1).
    """
    cost: int
    city: int
    tank: int
    canister: int

    def __lt__(self, other: 'State') -> bool:
        return self.cost < other.cost

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return (self.cost, self.city, self.tank, self.canister) == (other.cost, other.city, other.tank, other.canister)


class Graph:
    def __init__(self) -> None:
        """
        Класс, представляющий ненаправленный граф дорог между городами.
        """
        self._adjacency_list: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        """
        Добавляет ребро между городами u и v.
        Returns:
        """
        self._adjacency_list[u].append(v)
        self._adjacency_list[v].append(u)

    def get_neighbors(self, city: int) -> List[int]:
        return self._adjacency_list[city]


def min_fuel_cost(n: int, fuel_costs: List[int], graph: Graph) -> int:
    # Используем очередь с приоритетом
    pq: List[State] = [State(0, 1, 0, 0)]  # начинаем с города 1, пустой бак и канистра
    visited: Set[Tuple[int, int, int]] = set()

    while pq:
        state = heappop(pq)

        # Если добрались до города N, возвращаем стоимость
        if state.city == n:
            return state.cost

        # Проверка на повторное посещение состояния
        if (state.city, state.tank, state.canister) in visited:
            continue
        visited.add((state.city, state.tank, state.canister))

        # 1. Заправка только бака
        if state.tank == 0:
            heappush(pq, State(state.cost + fuel_costs[state.city - 1], state.city, 1, state.canister))

        # 2. Заправка бака и канистры
        if state.tank == 0 and state.canister == 0:
            heappush(pq, State(state.cost + 2 * fuel_costs[state.city - 1], state.city, 1, 1))

        # 3. Переливание бензина из канистры в бак
        if state.tank == 0 and state.canister > 0:
            heappush(pq, State(state.cost, state.city, 1, 0))

        # 4. Переход в соседний город (тратим 1 единицу топлива)
        if state.tank > 0:
            for neighbor in graph.get_neighbors(state.city):
                heappush(pq, State(state.cost, neighbor, state.tank - 1, state.canister))

    return -1  # Если не удалось добраться до города N


def main() -> None:
    n: int = int(input())
    fuel_costs: List[int] = list(map(int, input().split()))
    m: int = int(input())
    roads: List[Tuple[int, int]] = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(m)])

    graph = Graph()
    for u, v in roads:
        graph.add_edge(u, v)

    print(min_fuel_cost(n, fuel_costs, graph))


if __name__ == '__main__':
    main()
