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
from typing import List, Sequence, Tuple


def hungarian(cost_matrix: Sequence[Sequence[int]]) -> Sequence[Tuple[int, int]]:
    """
    Венгерский метод для задачи о назначениях.

    Венгерский метод — это комбинаторный оптимизационный алгоритм для задачи о назначениях.
    Алгоритм находит оптимальное распределение задач между исполнителями, минимизируя общую стоимость
    (например, время выполнения задач).

    Алгоритм работает с квадратной матрицей стоимости `cost_matrix` размера K x K, где:
    - Строки представляют исполнителей.
    - Столбцы представляют задачи.
    - Элементы матрицы представляют стоимость выполнения конкретной задачи конкретным исполнителем.

    ### Основные этапы алгоритма:
    1. **Инициализация потенциалов строк и столбцов:**
       Потенциалы строк и столбцов (`row_potentials` и `col_potentials`) инициализируются нулями.

    2. **Поиск минимального значения стоимости для текущей строки:**
       Для каждой строки матрицы определяется минимальная стоимость распределения с учётом текущих
       потенциалов и ранее выполненных назначений.

    3. **Обновление потенциалов:**
       Потенциалы строк и столбцов корректируются таким образом, чтобы уменьшить стоимость
       нераспределённых элементов, сохраняя назначение оптимальным.

    4. **Построение цепочки назначений:**
       Используется алгоритм поиска в ширину для обновления цепочки назначений на основе текущих
       минимальных стоимостей.

    5. **Обновление связей:**
       Обновляются связи (`task_assignment`), определяющие, какая задача назначена какому исполнителю.

    6. **Формирование результата:**
       Возвращается список пар, где каждая пара `(row, column)` указывает исполнителя и соответствующую
       задачу.

    ### Этапы работы функции:
    1. Определить количество задач `num_tasks` (размер матрицы).
    2. Инициализировать:
       - Потенциалы строк и столбцов (`row_potentials`, `col_potentials`).
       - Массив связей (`task_assignment`), изначально содержащий -1.
    3. Для каждой строки:
       - Вычислить минимальные стоимости для каждого столбца.
       - Построить цепочку назначений, обновляя связи на основе минимальных стоимостей.
       - Корректировать потенциалы строк и столбцов.
    4. Вернуть список оптимальных назначений в формате списка пар `(row, column)`.

    :param cost_matrix: Матрица K x K с временем решения задач участниками.
    :return: Список пар (строка, столбец), соответствующий оптимальному распределению.
    """
    num_tasks = len(cost_matrix)
    row_potentials = [0] * num_tasks  # Потенциалы строк
    col_potentials = [0] * num_tasks  # Потенциалы столбцов
    task_assignment = [-1] * num_tasks  # Связи (назначения) задач для каждого столбца

    for row in range(num_tasks):
        min_costs = [float('inf')] * num_tasks  # Минимальные стоимости для столбцов
        visited_columns = [False] * num_tasks  # Посещённые столбцы
        previous_columns = [-1] * num_tasks  # Предыдущие столбцы в цепочке
        current_row = row
        current_column = -1

        while current_row != -1:
            delta = float('inf')
            next_column = -1

            # Обновляем минимальные стоимости и находим наименьшую стоимость
            for col in filter(lambda x: not visited_columns[x], range(num_tasks)):
                reduced_cost = (
                        cost_matrix[current_row][col]
                        - row_potentials[current_row]
                        - col_potentials[col]
                )
                if reduced_cost < min_costs[col]:
                    min_costs[col] = reduced_cost
                    previous_columns[col] = current_column
                if min_costs[col] < delta:
                    delta = min_costs[col]
                    next_column = col

            # Корректируем потенциалы строк и столбцов
            for col in range(num_tasks):
                if visited_columns[col]:
                    row_potentials[task_assignment[col]] += delta
                    col_potentials[col] -= delta
                else:
                    min_costs[col] -= delta

            row_potentials[row] += delta
            visited_columns[next_column] = True
            current_column = next_column
            current_row = task_assignment[current_column]

        # Обновляем цепочку назначений
        while previous_columns[current_column] != -1:
            task_assignment[current_column] = task_assignment[previous_columns[current_column]]
            current_column = previous_columns[current_column]

        task_assignment[current_column] = row

    # Формируем список назначений
    return [(task_assignment[col], col) for col in range(num_tasks)]


def main() -> None:
    k: int = int(input())
    matrix: List[List[int]] = [list(map(int, input().split())) for _ in range(k)]
    result: Sequence[Tuple[int, int]] = hungarian(matrix)

    # Считаем минимальное время
    total_time: int = sum(matrix[row][col] for row, col in result)
    print(total_time)


if __name__ == "__main__":
    main()
