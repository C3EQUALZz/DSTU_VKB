import math

def find_shortest_path(coords):
    n = len(coords)
    # dp[mask][i] - минимальная длина пути, посещая вершины в маске `mask`, заканчиваясь в вершине `i`
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Начальная вершина посещена, длина пути 0

    # Заполнение dp-таблицы
    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):  # Если вершина u не посещена
                continue
            for v in range(n):
                if mask & (1 << v):  # Если вершина v уже посещена
                    continue
                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(
                    dp[next_mask][v],
                    dp[mask][u] + math.dist(coords[u], coords[v])
                )

    # Найти минимальную длину цикла
    min_path_length = float('inf')
    last_mask = (1 << n) - 1
    end_vertex = -1
    for u in range(1, n):
        cost = dp[last_mask][u] + math.dist(coords[u], coords[0])
        if cost < min_path_length:
            min_path_length = cost
            end_vertex = u

    # Восстановление пути
    path = []
    mask = last_mask
    current_vertex = end_vertex
    while current_vertex != 0:
        path.append(current_vertex)
        for prev_vertex in range(n):
            if (mask & (1 << prev_vertex)) and \
               math.isclose(dp[mask][current_vertex],
                            dp[mask ^ (1 << current_vertex)][prev_vertex] + math.dist(coords[prev_vertex], coords[current_vertex])):
                mask ^= (1 << current_vertex)
                current_vertex = prev_vertex
                break
    path.append(0)
    path.reverse()

    # Преобразование пути к нужному формату
    return min_path_length, [x + 1 for x in path[1:]]

def main():
    n = int(input())
    coords = [tuple(map(float, input().split())) for _ in range(n)]
    min_path_length, min_path = find_shortest_path(coords)
    print(f"{min_path_length:.14e}")
    print(' '.join(map(str, min_path)))

if __name__ == "__main__":
    main()
