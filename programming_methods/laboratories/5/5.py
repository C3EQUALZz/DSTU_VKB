from collections import defaultdict, deque


def edmonds_karp(n, edges):
    # Создаем граф с пропускными способностями
    capacity = defaultdict(lambda: defaultdict(int))
    for u, v, c in edges:
        capacity[u][v] += c  # Учитываем возможность нескольких рёбер между вершинами

    # Инициализация переменных
    source, sink = 1, n
    flow = 0

    while True:
        # BFS для поиска увеличивающего пути
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])
        path_flow = {source: float('Inf')}

        while queue:
            current = queue.popleft()
            for next_vertex in capacity[current]:
                if parent[next_vertex] == -1 and capacity[current][
                    next_vertex] > 0:  # Остаточная пропускная способность > 0
                    parent[next_vertex] = current
                    path_flow[next_vertex] = min(path_flow[current], capacity[current][next_vertex])
                    if next_vertex == sink:
                        break
                    queue.append(next_vertex)
            else:
                continue
            break

        # Если увеличивающий путь не найден, выходим из цикла
        if parent[sink] == -1:
            break

        # Увеличиваем поток по найденному пути
        increment = path_flow[sink]
        flow += increment
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= increment
            capacity[v][u] += increment
            v = u

    return flow


# Считывание входных данных
n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v, c = map(int, input().split())
    edges.append((u, v, c))

# Вычисление максимального потока
max_flow = edmonds_karp(n, edges)
print(max_flow)