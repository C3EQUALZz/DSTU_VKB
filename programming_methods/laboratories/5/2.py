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
    from_city: int
    to_city: int
    from_gate: int
    to_gate: int
    visited: bool = False


class CityGraph:
    def __init__(self, n: int, roads_data: List[Tuple[int, ...]]) -> None:
        self.n = n
        self.roads: List[Road] = []
        self.graph: List[List[int]] = [[] for _ in range(n + 1)]

        # Заполняем граф и список дорог
        for gate1, gate2 in roads_data:
            from_city = (gate1 + 3) // 4
            to_city = (gate2 + 3) // 4
            road_index = len(self.roads)
            self.graph[from_city].append(road_index)
            self.graph[to_city].append(road_index)
            self.roads.append(Road(from_city, to_city, gate1, gate2))

    def mark_road_visited(self, road_index: int) -> None:
        """Помечаем дорогу как посещенную."""
        self.roads[road_index].visited = True

    def __getitem__(self, city: int) -> List[int]:
        """Возвращает список дорог для данного города."""
        return self.graph[city]


def can_complete_task(n: int, graph: CityGraph) -> List[int]:
    stack = deque()  # Используем deque как стек
    ans = []  # Список ворот
    cur_city = 1

    while True:
        if not graph[cur_city]:  # Используем graph[cur_city] вместо graph.graph[cur_city]
            if not stack:
                break
            # Возвращаемся к предыдущему городу
            to_gate = stack.pop()
            from_gate = stack.pop()
            prev_city = stack.pop()
            ans.append(to_gate)
            ans.append(from_gate)
            cur_city = prev_city
            continue

        road_index = graph[cur_city][-1]  # Используем graph[cur_city] вместо graph.graph[cur_city]

        if graph.roads[road_index].visited:  # Если дорога уже посещена
            graph[cur_city].pop()  # Используем graph[cur_city] вместо graph.graph[cur_city]
            continue

        # Обновляем состояние дороги и перемещаемся в соседний город
        if cur_city == graph.roads[road_index].from_city:
            stack.extend([cur_city, graph.roads[road_index].from_gate, graph.roads[road_index].to_gate])
            graph.mark_road_visited(road_index)
            cur_city = graph.roads[road_index].to_city
        else:
            stack.extend([cur_city, graph.roads[road_index].to_gate, graph.roads[road_index].from_gate])
            graph.mark_road_visited(road_index)
            cur_city = graph.roads[road_index].from_city

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
