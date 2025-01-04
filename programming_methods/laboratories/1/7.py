"""
Задача №500. Парикмахерская

В парикмахерской работают три мастера. Каждый тратит на одного клиента ровно полчаса, а затем сразу переходит к
следующему, если в очереди кто-то есть, либо ожидает, когда придет следующий клиент.

Даны времена прихода клиентов в парикмахерскую (в том порядке, в котором они приходили).
Требуется для каждого клиента указать время, когда он выйдет из парикмахерской.

Входные данные

В первой строке вводится натуральное число N, не превышающее 100 – количество клиентов.
N строках вводятся времена прихода клиентов – по два числа, обозначающие часы и минуты (часы – от 0 до 23, минуты – от 0 до 59).
Времена указаны в порядке возрастания (все времена различны).

Гарантируется, что всех клиентов успеют обслужить до полуночи.

Выходные данные

Требуется вывести N пар чисел: времена выхода из парикмахерской 1-го, 2-го, …, N-го клиента (часы и минуты).
"""
from typing import List, Tuple


def calculate_exit_times(arrival_times: List[Tuple[int, ...]]) -> List[Tuple[int, int]]:
    workers_time: List[int] = [0, 0, 0]  # Время, когда каждый из трех мастеров свободен
    exit_times: List[Tuple[int, int]] = []  # Список для хранения времени выхода клиентов

    for hours, minutes in arrival_times:
        arrival_minutes = hours * 60 + minutes  # Преобразуем время прихода в минуты
        # Находим мастера, который свободен раньше всего
        next_worker_index = workers_time.index(min(workers_time))

        # Если мастер свободен до прихода клиента, обновляем его время
        if workers_time[next_worker_index] <= arrival_minutes:
            workers_time[next_worker_index] = arrival_minutes + 30
        else:
            workers_time[next_worker_index] += 30  # Мастер начинает работать сразу после завершения

        # Сохраняем время выхода клиента в формате (часы, минуты)
        exit_time = workers_time[next_worker_index]
        exit_times.append((exit_time // 60, exit_time % 60))

    return exit_times


def main() -> None:
    n: int = int(input())
    arrival_times: List[Tuple[int, ...]] = [tuple(map(int, input().split())) for _ in range(n)]

    # Получение времени выхода клиентов
    exit_times = calculate_exit_times(arrival_times)

    # Вывод результата
    for hours, minutes in exit_times:
        print(hours, minutes)


if __name__ == '__main__':
    main()
