"""
Задача №180. Цикл

Дан ориентированный граф. Определить, есть ли в нем цикл отрицательного веса, и если да, то вывести его.
Входные данные

В первой строке содержится число N (1 <= N <= 100) – количество вершин графа.
В следующих N строках находится по N чисел – матрица смежности графа.
Веса ребер по модулю меньше 100000. Если ребра нет, соответствующее значение равно 100000.

Выходные данные

В первой строке выведите "YES", если цикл существует, или "NO", в противном случае.
При наличии цикла выведите во второй строке количество вершин в нем (считая одинаковые – первую и последнюю),
а в третьей строке – вершины, входящие в этот цикл, в порядке обхода. Если циклов несколько, то выведите любой из них.
"""
INF = float('inf')

n = int(input())

adj_list = [
    (w, (i, j))
    for i in range(n)
    for j, w in enumerate(map(int, input().split()))
    if w < 100000
]

distance = [INF] * n
used = [0] * n
path = [-1] * n
cycle = -1

for k in range(n):
    if distance[k] == INF:
        distance[k] = 0
        for i in range(n):
            cycle = -1
            for j in range(len(adj_list)):
                if distance[adj_list[j][1][0]] < INF:
                    if distance[adj_list[j][1][1]] > distance[adj_list[j][1][0]] + adj_list[j][0]:
                        distance[adj_list[j][1][1]] = distance[adj_list[j][1][0]] + adj_list[j][0]
                        path[adj_list[j][1][1]] = adj_list[j][1][0]
                        cycle = adj_list[j][1][0]

if cycle == -1:
    print("NO")
else:
    print("YES")
    cycle = path[path.index(cycle)]
    cycle_start = cycle
    p = [cycle]
    cycle = path[cycle]
    while cycle != cycle_start:
        p.append(cycle)
        cycle = path[cycle]
    p.append(cycle_start)
    print(len(p))
    p.reverse()
    for node in p:
        print(node + 1, end=' ')
