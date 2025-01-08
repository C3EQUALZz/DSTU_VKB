"""
Задача №394. K задач (A)

K участникам сборов для решения было предложено K задач.
Участники решили разделить задачи между собой, решить каждому по одной задаче, а затем обменяться решениями
(они не учли, что система ejudge способна отследить данный факт J).
Известно ориентировочное время, за которое каждый из участников сборов может решить каждую из предложенных задач.

Помогите участникам сборов распределить задачи так (по одной каждому участнику),
чтобы суммарное время, потраченное на их решение было минимальным.

Входные данные

Во входном файле сначала записано число K (0 < K < 101) и далее K2 неотрицательных целых чисел,
не превосходящие 20000, описывающих матрицу K x K, времен решения каждым из участников каждой из задач.

Выходные данные

В файл выведите суммарное минимальное время решения всех задач, при условии, что каждый участник решит ровно одну задачу.
"""

def hungarian(matrix):
    """
    Реализует венгерский метод для задачи о назначениях.
    :param matrix: Прямоугольная матрица (список списков), не обязательно положительные числа.
                   Высота матрицы должна быть меньше либо равна ширине.
    :return: Список выбранных элементов, по одному из каждой строки.
    """
    height = len(matrix)
    width = len(matrix[0])

    # Значения, вычитаемые из строк (u) и столбцов (v)
    u = [0] * height
    v = [0] * width

    # Индекс помеченной клетки в каждом столбце
    mark_indices = [-1] * width

    for i in range(height):
        links = [-1] * width
        mins = [float('inf')] * width
        visited = [0] * width

        marked_i = i
        marked_j = -1
        j = -1

        while marked_i != -1:
            # Обновление информации о минимумах и выбор наименьшего элемента
            j = -1
            for j1 in range(width):
                if not visited[j1]:
                    diff = matrix[marked_i][j1] - u[marked_i] - v[j1]
                    if diff < mins[j1]:
                        mins[j1] = diff
                        links[j1] = marked_j
                    if j == -1 or mins[j1] < mins[j]:
                        j = j1

            # Манипуляции с матрицей для обнуления текущего элемента
            delta = mins[j]
            for j1 in range(width):
                if visited[j1]:
                    u[mark_indices[j1]] += delta
                    v[j1] -= delta
                else:
                    mins[j1] -= delta
            u[i] += delta

            # Переход к следующей итерации, если коллизия не разрешена
            visited[j] = 1
            marked_j = j
            marked_i = mark_indices[j]

        # Обновление отметок на чередующейся цепочке
        while links[j] != -1:
            mark_indices[j] = mark_indices[links[j]]
            j = links[j]
        mark_indices[j] = i

    # Формирование результата
    result = [(mark_indices[j], j) for j in range(width) if mark_indices[j] != -1]
    return result


def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    k = int(data[0])
    matrix = []
    idx = 1
    for i in range(k):
        matrix.append([int(data[idx + j]) for j in range(k)])
        idx += k

    # Применяем венгерский метод
    result = hungarian(matrix)

    # Считаем минимальное время
    total_time = sum(matrix[row][col] for row, col in result)
    print(total_time)


if __name__ == "__main__":
    main()