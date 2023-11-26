from itertools import combinations


def question():
    try:
        name = int(input('Введите число задания '))
    except:
        print('Вы ввели не число. Запускаю заново.')
        question()
    if name == 1:

        try:
            n = int(input('Введите количество вершин '))
        except:
            print('Вы ввели не число. Запускаю заново.')
            question()
        matrix_print(n)

        try:
            start = int(input('С какой точки начать поиск в глубину у графа? '))
            end = int(input('В какую точку нужно прийти? '))
        except:
            print('Вы ввели не число. Запуска заново.')
            question()
        dfs(start, end, graphs(stats), [], set())

    elif name == 2:
        try:
            start = (input('Введите точку, с которой начинается алгоритм Дейкстры. Буква от a до f '))
            end = (input('Введите конечную точку. Буква от a до f '))
        except:
            print('Вы ввели не букву. Запускаю заново.')
            question()
        dejkstra(start, end)

    else:
        print('Неверно введено задание. Заново?')
        if input() in ['Да', 'да', 'дА', 'ДА']:
            question()
        else:
            exit()


### 1 задание
def matrix_print(n):
    global stats
    matrix = [[0 for x in range(n)] for _ in range(n)]
    stats = list(map(list, combinations([x for x in range(1, n + 1)], 2)))
    i = 0
    while i != len(stats):
        if input(f'Есть ли вершина между {stats[i][0]} и {stats[i][1]} ') in ['Да', 'да', 'дА', 'ДА']:
            matrix[stats[i][0] - 1][stats[i][1] - 1] = 1
            matrix[stats[i][1] - 1][stats[i][0] - 1] = 1
            i += 1
        else:
            stats.remove(stats[i])
    print(' ', *[x for x in range(1, n + 1)])
    t = 1
    for r in matrix:
        print(t, *r)
        t += 1
    return stats


def graphs(stats):
    d = {}
    for pair in stats:
        if pair[0] in d.keys():
            d[pair[0]].append(pair[1])
        else:
            d.update({pair[0]: [pair[1]]})

        if pair[1] in d.keys():
            d[pair[1]].append(pair[0])
        else:
            d.update({pair[1]: [pair[0]]})
    return d


def dfs(start, end, graphs, data, visited):
    if len(data) == 0:
        data.append(start)
        visited.add(start)

    if start == end:
        return print(f'Путь - {data}, а количество ребер {len(data) - 1}')

    for next in set(graphs[start]) - visited:
        data.append(next)
        visited.add(next)
        dfs(next, end, graphs, data, visited)
        data.pop()
        visited.remove(next)


###2 задание
def dejkstra(start, end):
    graph = {
        'a': {'b': 5, 'c': 2},
        'b': {'a': 5, 'c': 7, 'd': 8},
        'c': {'a': 2, 'b': 7, 'd': 4, 'e': 8, },
        'd': {'b': 8, 'c': 4, 'e': 6, 'f': 4, },
        'e': {'c': 8, 'd': 6, 'f': 3},
        'f': {'e': 3, 'd': 4}
    }
    shortest_distances = {i: float('inf') for i in graph}
    shortest_distances[start] = 0
    path = {}  # самые короткий путь для каждой точки, здесь именно буква
    travel = []  # наша траектория движения.

    while len(graph) > 0:
        min_node = None
        for current_node in graph:
            if min_node == None:
                min_node = current_node
            elif shortest_distances[min_node] > shortest_distances[current_node]:
                min_node = current_node
        for node, value in graph[min_node].items():
            if value + shortest_distances[min_node] < shortest_distances[node]:
                shortest_distances[node] = value + shortest_distances[min_node]
                path[node] = min_node
        graph.pop(min_node)
    ###Восстановление пути из словаря. Каждый раз так возвращаем.
    while end != start:
        try:
            travel.insert(0, end)
            end = path[end]
        except:
            print('Невозможно восстановить путь.')
            break
    travel.insert(0, start)
    if shortest_distances[min_node] != float('inf'):
        return print(f'Минимальный путь - {travel}, а самая минимальная сумма - {shortest_distances[min_node]}')


while True:
    if __name__ == "__main__":
        question()
