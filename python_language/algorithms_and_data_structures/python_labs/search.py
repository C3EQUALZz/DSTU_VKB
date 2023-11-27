from itertools import combinations


def binary_search(search_list, search_value):
    spisok = search_list
    high, low, middle = len(spisok) - 1, 0, 0
    while low <= high and middle != search_value:
        middle = (low + high) // 2
        guess = spisok[middle]
        if guess == search_value:
            return middle
        elif guess > search_value:
            high = middle - 1
        else:
            low = middle + 1
    else:
        return 'Элемент в массиве не найден'


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


def depth_first_search(start, end):
    try:
        n = int(input('Введите количество вершин '))
    except ValueError:
        print('Вы ввели не число. Запускаю заново. ')
        depth_first_search()

    def matrix_print(n):
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
        return stats

    stats = matrix_print(n)

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

    return dfs(start, end, graphs(stats), [], set())


def search_dejkstra(start, end):
    try:
        m = int(input('Введите количесиво вершин: '))
    except ValueError:
        print('Вы ввели не int число')
        search_dejkstra(start, end)

    def matr(m):
        matr = {}
        for i, j in combinations([x for x in range(1, m + 1)], 2):
            try:
                a = int(input(
                    f'Введите расстояние между вершиной {chr(ord("A") + i - 1)} и {chr(ord("A") + j - 1)} (если связи нет введите {0}): '))
            except ValueError:
                matr(m)

            if a != 0:
                try:
                    matr[chr(ord("A") + i - 1)].update({f'{chr(ord("A") + j - 1)}': int(a)})
                except KeyError:
                    matr[chr(ord("A") + i - 1)] = {f'{chr(ord("A") + j - 1)}': int(a)}
                try:
                    matr[chr(ord("A") + j - 1)].update({f'{chr(ord("A") + i - 1)}': int(a)})
                except KeyError:
                    matr[chr(ord("A") + j - 1)] = {f'{chr(ord("A") + i - 1)}': int(a)}
        return matr

    graph = matr(m)

    def dejkstra(start, end, graph):
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

    return dejkstra(start, end, graph)
