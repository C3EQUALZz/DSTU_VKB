"""
Задача №1704. Маршрут для гонца

В королевстве N; городов, пронумерованных от 1 до N. Столица имеет номер 1.
Каждый город окружен городской стеной с 4 воротами.
Ворота пронумерованы следующим образом: ворота i-го города (1 ≤ i ≤ N) имеют номера 4i−3, 4i−2, 4i−1, 4i.
Через каждые ворота проходит ровно 1 дорога, которая ведет до некоторых ворот другого города
(заметьте, что может существовать несколько дорог между двумя городами).
По всем дорогам можно двигаться в обоих направлениях. Благодаря системе туннелей и мостов дороги не пересекаются вне городов.

Королевский гонец должен развесить копии Очень важного Королевского Указа на внешней стороне всех ворот каждого города.
Гонец может свободно передвигаться от одних ворот к другим в пределах города, но вне города он может двигаться только по дорогам.
Гонец выезжает из столицы и должен туда вернуться после выполнения задания.

Может ли гонец выполнить поручение, проходя через каждые ворота только один раз?
Выход из города через ворота только для того, чтобы вывесить на их внешней стороне указ,
а затем немедленное возвращение в город, считается за один проход через ворота.

Входные данные

Первая строка входного файла содержит целое число N (2 ≤ N ≤ 1000).
Каждая из последующих 2N строк описывает одну дорогу и содержит 2 целых числа, разделенных
пробелом: номера ворот, соединенных дорогой.

Выходные данные

В первую строку выходного файла выведите Yes или No в зависимости от того, может ли поручение гонца быть выполнено,
если проходить через ворота только один раз.
В случае если это возможно, вторая строка выходного файла должна содержать 4N целых чисел,
разделенных пробелом: номера ворот в порядке прохождения через них гонцом.
Если существует несколько решений, выведите любое из них.
"""
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Road:
    city1: int
    city2: int
    gate1: int
    gate2: int
    visited: bool = False


class CityGraph:
    def __init__(self, n: int, roads_data: List[Tuple[int, ...]]) -> None:
        self.n = n
        self.roads: List[Road] = []
        self.graph: List[List[int]] = [[] for _ in range(n + 1)]

        # Заполняем граф и список дорог
        for gate1, gate2 in roads_data:
            city1 = (gate1 + 3) // 4
            city2 = (gate2 + 3) // 4
            road_index = len(self.roads)
            self.graph[city1].append(road_index)
            self.graph[city2].append(road_index)
            self.roads.append(Road(city1, city2, gate1, gate2))

    def mark_road_visited(self, road_index: int) -> None:
        """Помечаем дорогу как посещенную."""
        self.roads[road_index].visited = True


def can_complete_task(n: int, graph: CityGraph) -> List[int]:
    stack = deque()  # Используем deque как стек
    ans = []  # Список ворот
    cur_city = 1

    while True:
        if not graph.graph[cur_city]:
            if not stack:
                break
            # Возвращаемся к предыдущему городу
            gates2 = stack.pop()
            gates1 = stack.pop()
            prev_city = stack.pop()
            ans.append(gates2)
            ans.append(gates1)
            cur_city = prev_city
            continue

        road_index = graph.graph[cur_city][-1]

        if graph.roads[road_index].visited:  # Если дорога уже посещена
            graph.graph[cur_city].pop()
            continue

        # Обновляем состояние дороги и перемещаемся в соседний город
        if cur_city == graph.roads[road_index].city1:
            stack.extend([cur_city, graph.roads[road_index].gate1, graph.roads[road_index].gate2])
            graph.mark_road_visited(road_index)
            cur_city = graph.roads[road_index].city2
        else:
            stack.extend([cur_city, graph.roads[road_index].gate2, graph.roads[road_index].gate1])
            graph.mark_road_visited(road_index)
            cur_city = graph.roads[road_index].city1

    # Проверяем, удалось ли пройти через все ворота
    return ans if len(ans) == 4 * n else []


def main() -> None:
    n = int(input())
    roads_data = [tuple(map(int, input().split())) for _ in range(2 * n)]

    graph = CityGraph(n, roads_data)

    result = can_complete_task(n, graph)

    if result:
        print("Yes", " ".join(map(str, result)), sep="\n")
    else:
        print("No")


if __name__ == "__main__":
    main()
