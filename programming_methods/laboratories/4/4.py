"""
Задача №1928. Производство деталей

Предприятие «Авто-2010» выпускает двигатели для известных во всём мире автомобилей.
Двигатель состоит ровно из n деталей, пронумерованных от 1 до n, при этом деталь с номером i изготавливается за pi секунд.
Специфика предприятия «Авто-2010» заключается в том, что там одновременно может изготавливаться лишь одна деталь двигателя.
Для производства некоторых деталей необходимо иметь предварительно изготовленный набор других деталей.

Генеральный директор «Авто-2010» поставил перед предприятием амбициозную задачу — за наименьшее время изготовить
деталь с номером 1, чтобы представить её на выставке.

Требуется написать программу, которая по заданным зависимостям порядка производства между деталями найдёт наименьшее время,
за которое можно произвести деталь с номером 1.

Входные данные

Первая строка входного файла содержит число n (1≤n≤100000) — количество деталей двигателя.
Вторая строка содержит n натуральных чисел p1,p2,…,pn, определяющих время изготовления каждой детали в секундах.
Время для изготовления каждой детали не превосходит 10^9 секунд.

Каждая из последующих n строк входного файла описывает характеристики производства деталей.
Здесь i-я строка содержит число деталей ki, которые требуются для производства детали с номером i, а также их номера.
В i-й строке нет повторяющихся номеров деталей. Сумма всех чисел ki не превосходит 200000.

Известно, что не существует циклических зависимостей в производстве деталей.

Выходные данные

В первой строке выходного файла должны содержаться два числа: минимальное время (в секундах),
необходимое для скорейшего производства детали с номером 1 и число k деталей, которые необходимо для этого произвести.
Во второй строке требуется вывести через пробел k чисел — номера деталей в том порядке, в котором следует их производить
для скорейшего производства детали с номером 1.
"""
from typing import List, Tuple
from collections import deque


def produce_part(
        part_id: int,
        production_times: List[int],
        dependencies: List[List[int]],
        produced: List[bool],
        production_order: deque
) -> int:

    if produced[part_id]:
        return 0

    produced[part_id] = True
    total_time = production_times[part_id]  # Время на изготовление текущей детали

    for dependency in dependencies[part_id - 1]:  # Индексация зависит от 0
        total_time += produce_part(dependency, production_times, dependencies, produced, production_order)

    production_order.append(part_id)
    return total_time


def calculate_minimum_production_time(
        n: int,
        production_times: List[int],
        dependencies: List[List[int]]
) -> Tuple[int, List[int]]:

    produced = [False] * (n + 1)
    production_order = deque()

    total_time = produce_part(1, production_times, dependencies, produced, production_order)

    return total_time, list(production_order)


def main() -> None:
    n = int(input())
    production_times = [0] + list(map(int, input().split()))
    dependencies = [list(map(int, input().split()[1:])) for _ in range(n)]

    total_time, order = calculate_minimum_production_time(n, production_times, dependencies)

    print(total_time, len(order))
    print(*order)


if __name__ == "__main__":
    main()
