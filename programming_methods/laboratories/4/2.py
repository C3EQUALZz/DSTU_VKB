"""
Задача №165. Банкет

На банкет были приглашены N Очень Важных Персон (ОВП).
Были поставлены 2 стола. Столы достаточно большие, чтобы все посетители банкета могли сесть за любой из них.
Проблема заключается в том, что некоторые ОВП не ладят друг с другом и не могут сидеть за одним столом.
Вас попросили определить, возможно ли всех ОВП рассадить за двумя столами.

Входные данные

В первой строке входных данных содержатся два числа: N и M (1 <= N, M <= 100),
где N – количество ОВП, а M – количество пар ОВП, которые не могут сидеть за одним столом.
В следующих M строках записано по 2 числа – пары ОВП, которые не могут сидеть за одним столом.

Выходные данные

Если способ рассадить ОВП существует, то выведите YES в первой строке и номера ОВП, которых необходимо посадить за
первый стол, во второй строке. В противном случае в первой и единственной строке выведите NO.
"""
from typing import List, Tuple


def build_graph(n: int, pairs: List[Tuple[int, ...]]) -> List[List[int]]:
    graph = [[] for _ in range(n)]
    for u, v in pairs:
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)
    return graph


def can_seat_vips(graph: List[List[int]], n: int) -> Tuple[bool, List[int]]:
    color = [-1] * n  # -1: uncolored, 0: table 1, 1: table 2
    for i in range(n):
        if color[i] == -1:  # If the vertex is uncolored, start DFS
            stack = [i]
            color[i] = 0  # Color the vertex with color 0
            while stack:
                v = stack.pop()
                for u in graph[v]:
                    if color[u] == -1:  # If the neighbor is uncolored
                        stack.append(u)
                        color[u] = 1 - color[v]  # Color it with the opposite color
                    elif color[u] == color[v]:  # If the neighbor has the same color
                        return False, []  # Seating is impossible
    # Collect vertices for table 1
    table1 = [i + 1 for i in range(n) if color[i] == 0]
    return True, table1


def main() -> None:
    n, m = map(int, input().split())
    pairs = [tuple(map(int, input().split())) for _ in range(m)]

    graph = build_graph(n, pairs)
    possible, table1 = can_seat_vips(graph, n)

    if possible:
        print("YES")
        print(*table1)
    else:
        print("NO")


if __name__ == "__main__":
    main()
