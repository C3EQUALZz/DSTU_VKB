"""
Задача №2983. Баржа

На барже располагается K грузовых отсеков.
В каждый отсек можно поместить некоторое количество бочек с одним из 10000 видов топлива.
Причём извлечь бочку из отсека можно лишь в случае, если все бочки, помещённые в этот отсек после неё, уже были извлечены.
Таким образом в каждый момент времени в каждом непустом отсеке имеется ровно одна бочка, которую можно извлечь не трогая остальных.
Будем называть такие бочки крайними.

Изначально баржа пуста.
Затем она последовательно проплывает через N доков, причём в каждом доке на баржу либо погружается бочка с некоторым
видом топлива в некоторый отсек, либо выгружается крайняя бочка из некоторого отсека.
Однако, если указанный отсек пуст, либо если выгруженная бочка содержит не тот вид топлива, который ожидалось,
следует зафиксировать ошибку.
Если на баржу оказывается погружено более P бочек или если после прохождения всех доков она не стала пуста,
следует также зафиксировать ошибку.
От вас требуется либо указать максимальное количество бочек, которые одновременно пребывали на барже либо зафиксировать ошибку.
"""

from collections import deque
from typing import List, Deque


def process_docks(docks: int, cells: int, max_len: int) -> int:
    max_tanks: int = 0
    current_tanks: int = 0
    error: bool = False

    # Инициализация отсеков
    cell: List[Deque[str]] = [deque() for _ in range(cells)]

    # Обработка действий в доках
    for _ in range(docks):
        action: List[str] = input().split()
        if action[0] == "+":
            # Загрузка бочки
            cell_index: int = int(action[1]) - 1
            fuel_type: str = action[2]
            cell[cell_index].append(fuel_type)
            current_tanks += 1

            if current_tanks > max_len:
                error = True
                break
            max_tanks = max(max_tanks, current_tanks)
        else:
            # Выгрузка бочки
            cell_index: int = int(action[1]) - 1
            fuel_type: str = action[2]

            if not cell[cell_index] or cell[cell_index].pop() != fuel_type:
                error = True
                break
            current_tanks -= 1

    return -1 if current_tanks > 0 or error else max_tanks


def main() -> None:
    # Чтение входных данных
    request: List[str] = input().split()
    docks: int = int(request[0])
    cells: int = int(request[1])
    max_len: int = int(request[2])

    result: int = process_docks(docks, cells, max_len)

    print("Error" if result == -1 else result)


if __name__ == "__main__":
    main()
