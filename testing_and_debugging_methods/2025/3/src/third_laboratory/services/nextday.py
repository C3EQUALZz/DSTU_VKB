"""Исправленная реализация функции расчёта следующей даты.

Исходная версия (см. ``nextday_legacy.py``) имела сигнатуру
``next_day(day, month, year)``, тогда как вызов в коде запуска
(см. Рисунок 5 задания) был выполнен в порядке
``nextday.next_day(year, month, day)``. Из-за рассогласования при
вводе ``year=2023, month=11, day=10`` функция получала
``day=2023, month=11, year=10``, что приводило к ``None``
(день > количества дней в ноябре).

Здесь сигнатура приведена к естественному порядку
``next_day(year, month, day)`` — от старшего поля к младшему,
как в ``datetime.date(year, month, day)``. Это совпадает с тем,
как функция фактически вызывалась в Рисунке 5, поэтому баг
устраняется без правки вызывающего кода.
"""

from __future__ import annotations

from typing import Optional

DateTuple = tuple[int, int, int]


def is_leap_year(year: int) -> bool:
    """Проверка года на високосность по григорианскому правилу."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(month: int, year: int) -> Optional[int]:
    """Количество дней в месяце с учётом високосного года.

    Возвращает ``None``, если ``month`` вне диапазона ``1..12``.
    """
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return None


def next_day(year: int, month: int, day: int) -> Optional[DateTuple]:
    """Возвращает дату, следующую за заданной, в виде кортежа ``(year, month, day)``.

    Возвращает ``None`` для любых некорректных входных данных:
        * не-целочисленный тип (``bool`` тоже считается некорректным);
        * year < 1;
        * month вне диапазона 1..12;
        * day вне диапазона 1..days_in_month(month, year).
    """
    # Тип: только int, bool отдельно отвергаем (bool — подкласс int).
    for value in (year, month, day):
        if isinstance(value, bool) or not isinstance(value, int):
            return None

    if year < 1 or month < 1 or month > 12 or day < 1:
        return None

    max_days = days_in_month(month, year)
    if max_days is None or day > max_days:
        return None

    if day < max_days:
        # Обычный день: остаёмся в том же месяце.
        return (year, month, day + 1)
    if month < 12:
        # Последний день месяца, но не декабря.
        return (year, month + 1, 1)
    # Последний день декабря — переход к следующему году.
    return (year + 1, 1, 1)
