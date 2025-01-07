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
import heapq
from typing import List, Tuple, Dict, Set
from collections import defaultdict


class Graph:
    def __init__(self) -> None:
        self.adjacency_list: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

    def get_neighbors(self, city: int) -> List[int]:
        return self.adjacency_list[city]


def min_fuel_cost(n: int, fuel_costs: List[int], graph: Graph) -> int:
    # Состояние: (стоимость, город, топливо в баке, топливо в канистре)
    # Используем очередь с приоритетом
    pq: List[Tuple[int, int, int, int]] = [(0, 1, 0, 0)]  # начинаем с города 1, пустой бак и канистра
    visited: Set[Tuple[int, int, int]] = set()

    while pq:
        cost, city, tank, canister = heapq.heappop(pq)

        # Если добрались до города N, возвращаем стоимость
        if city == n:
            return cost

        # Проверка на повторное посещение состояния
        if (city, tank, canister) in visited:
            continue
        visited.add((city, tank, canister))

        # 1. Заправка только бака
        if tank == 0:
            heapq.heappush(pq, (cost + fuel_costs[city - 1], city, 1, canister))

        # 2. Заправка бака и канистры
        if tank == 0 and canister == 0:
            heapq.heappush(pq, (cost + 2 * fuel_costs[city - 1], city, 1, 1))

        # 3. Переливание бензина из канистры в бак
        if tank == 0 and canister > 0:
            heapq.heappush(pq, (cost, city, 1, 0))

        # 4. Переход в соседний город (тратим 1 единицу топлива)
        if tank > 0:
            for neighbor in graph.get_neighbors(city):
                heapq.heappush(pq, (cost, neighbor, tank - 1, canister))

    return -1  # Если не удалось добраться до города N


def main() -> None:
    # Ввод данных
    n = int(input())
    fuel_costs = list(map(int, input().split()))
    m = int(input())
    roads = [tuple(map(int, input().split())) for _ in range(m)]

    graph = Graph()
    for u, v in roads:
        graph.add_edge(u, v)

    # Вывод результата
    print(min_fuel_cost(n, fuel_costs, graph))


if __name__ == '__main__':
    main()
