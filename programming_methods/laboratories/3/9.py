"""
Задача №3088. Золотые слитки

Даны N золотых слитков известных масс.
Определите, какую наибольшую массу золота можно унести, если вместимость рюкзака не превышает S.

Входные данные

Программа получает на вход целое число S — вместимость рюкзака, не превосходящее 10000 и количество слитков N,
не превосходящее 300. Далее следует N целых неотрицательных чисел, не превосходящих 100000 — веса слитков.

Выходные данные

Программа должна вывести единственное целое число — максимально возможных вес золота, который поместится в данный рюкзак.
"""


def max_gold_weight(capacity: int, weights: list) -> int:
    """Определяет максимальный вес золота, который можно унести в рюкзак."""
    # Инициализация массива для хранения достижимых весов
    achievable_weights = [0] * (capacity + 1)
    achievable_weights[0] = 1  # Нулевой вес всегда достижим

    # Проходим по каждому слитку
    for weight in weights:
        # Обновляем массив достижимых весов в обратном порядке
        for current_capacity in range(capacity, weight - 1, -1):
            if achievable_weights[current_capacity - weight] == 1:
                achievable_weights[current_capacity] = 1

    # Находим максимальный вес, который можно унести
    for i in range(capacity, -1, -1):
        if achievable_weights[i] == 1:
            return i  # Возвращаем максимальный вес

    return 0  # Если ничего не удалось унести


def main():
    capacity, n = map(int, input().split())
    weights = list(map(int, input().split()))

    max_weight = max_gold_weight(capacity, weights)
    print(max_weight)


if __name__ == "__main__":
    main()
