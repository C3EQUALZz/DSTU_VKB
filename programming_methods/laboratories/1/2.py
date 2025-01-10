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
from typing import List, Deque, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    """
    Класс, который описывает действие с текущей строки ввода
    - operation - "+" для загрузки, "-" для выгрузки
    - cell_index - Индекс отсека (по задаче начинается с 1)
    - fuel_type - Тип топлива (для выгрузки)
    """
    operation: str
    cell_index: int
    fuel_type: str


def process_docks(cells: int, max_len: int, actions: Iterable[Action]) -> int:
    """
    Здесь у нас динамическое программирование, где каждое следующее явление зависит от прошлого.
    Когда сказали: "Причём извлечь бочку из отсека можно лишь в случае, если все бочки, помещённые в этот отсек после неё,
    уже были извлечены", то становится понятным, что надо оперировать стеком, где есть LIFO. В Python нет готового стека.
    Использовать list не так эффективно, потому что тут используется под капотом массив, а не связный список.
    Поэтому здесь используется дек, который мы "ужимаем" до стека.

    :param cells: Количество отсеков.
    :param max_len: Ограничение на количество бочек на барже.
    :param actions: все операции, которые даны по условию. Например, "+ 1 1".

    :returns: Максимальное количество бочек, которые одновременно пребывали на барже.
     Если количество -1, то будет выведена ошибка.
    """
    max_tanks: int = 0
    current_tanks: int = 0
    error: bool = False

    cell: List[Deque[str]] = [deque() for _ in range(cells)]

    for action in actions:
        if action.operation == "+":
            # Загрузка бочки
            cell_index: int = action.cell_index - 1
            cell[cell_index].append(action.fuel_type)
            current_tanks += 1

            if current_tanks > max_len:
                error = True
                break
            max_tanks = max(max_tanks, current_tanks)
        else:
            # Выгрузка бочки
            cell_index: int = action.cell_index - 1

            if not cell[cell_index] or cell[cell_index].pop() != action.fuel_type:
                error = True
                break
            current_tanks -= 1

    return -1 if current_tanks > 0 or error else max_tanks


def main() -> None:
    request: List[str] = input().split()
    docks: int = int(request[0])
    cells: int = int(request[1])
    max_len: int = int(request[2])

    actions: List[Action] = []
    for _ in range(docks):
        action_data: List[str] = input().split()
        action = Action(operation=action_data[0], cell_index=int(action_data[1]), fuel_type=action_data[2])
        actions.append(action)

    result: int = process_docks(cells, max_len, actions)

    print("Error" if result == -1 else result)


if __name__ == "__main__":
    main()
