"""Исправленная версия расчёта среднего арифметического."""


def average(values: list[float]) -> float:
    """Вычислить среднее арифметическое непустого списка."""
    if not values:
        raise ValueError("Список не должен быть пустым")
    total = 0.0
    for index in range(len(values)):
        total += values[index]
    return total / len(values)
