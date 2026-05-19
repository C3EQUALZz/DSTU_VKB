"""Оригинальная (дефектная) версия из задания.

Сигнатура — ``next_day(day, month, year)``. Сохраняется для
демонстрации бага: в коде запуска вызов выполнен в порядке
``next_day(year, month, day)``, и при ``year=2023, month=11, day=10``
функция получает на вход ``day=2023, month=11, year=10`` и возвращает
``None``.

Этот модуль используется только в тестах ``test_legacy_bug.py``
для фиксации наблюдаемого дефекта.
"""

from __future__ import annotations

from typing import Optional

from third_laboratory.services.nextday import days_in_month

DateTuple = tuple[int, int, int]


def next_day(day, month, year) -> Optional[DateTuple]:
    """Исходная функция из задания — обратите внимание на порядок параметров."""
    # Validate input
    if (
        not isinstance(day, int)
        or not isinstance(month, int)
        or not isinstance(year, int)
    ):
        return None

    if year < 1 or month < 1 or month > 12 or day < 1:
        return None

    max_days = days_in_month(month, year)
    if max_days is None or day > max_days:
        return None

    # Calculate next day
    if day < max_days:
        # Not the last day of month
        return (day + 1, month, year)
    elif month < 12:
        # Last day of month, but not December
        return (1, month + 1, year)
    else:
        # Last day of year
        return (1, 1, year + 1)
