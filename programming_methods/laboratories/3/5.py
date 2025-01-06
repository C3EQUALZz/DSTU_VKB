"""
Задача №3090. Рюкзак с восстановлением ответа (C)

Дано N предметов массой m1, …, mN и стоимостью c1, …, cN соответственно.

Ими наполняют рюкзак, который выдерживает вес не более M.
Определите набор предметов, который можно унести в рюкзаке, имеющий наибольшую стоимость.

Входные данные

В первой строке вводится натуральное число N, не превышающее 100 и натуральное число M, не превышающее 10000.

Во второй строке вводятся N натуральных чисел mi, не превышающих 100.

В третьей строке вводятся N натуральных чисел сi, не превышающих 100.

Выходные данные

Выведите номера предметов (числа от 1 до N), которые войдут в рюкзак наибольшей стоимости.
"""


def knapsack(n: int, m: int, weights: list, costs: list) -> list:
    """Решает задачу о рюкзаке и возвращает набор предметов с наибольшей стоимостью."""
    # Инициализация таблицы для динамического программирования
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Заполнение таблицы
    for n in range(1, n + 1):
        for m in range(m + 1):
            dp[n][m] = dp[n - 1][m]  # Не берем текущий предмет
            if m >= weights[n] and dp[n - 1][m - weights[n]] + costs[n] > dp[n][m]:
                dp[n][m] = dp[n - 1][m - weights[n]] + costs[n]  # Берем текущий предмет

    # Восстановление набора предметов
    selected_items = []
    remaining_weight = m
    for n in range(n, 0, -1):
        if dp[n][remaining_weight] != dp[n - 1][remaining_weight]:  # Если предмет n был выбран
            selected_items.append(n)  # Добавляем номер предмета
            remaining_weight -= weights[n]  # Уменьшаем оставшийся вес

    return selected_items[::-1]  # Возвращаем в правильном порядке


def main() -> None:
    n, m = map(int, input().split())
    weights = [0] + list(map(int, input().split()))
    costs = [0] + list(map(int, input().split()))

    selected_items = knapsack(n, m, weights, costs)

    # Выводим результат
    print(' '.join(map(str, selected_items)))


if __name__ == "__main__":
    main()
