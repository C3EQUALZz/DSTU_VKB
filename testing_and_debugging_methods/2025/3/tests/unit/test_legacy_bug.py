"""Тесты-«пугалки» для бага из задания.

Дефект (см. README, Задание №2):
    * сигнатура исходной функции:   ``next_day(day, month, year)``
    * вызов в коде запуска:         ``next_day(year, month, day)``
    Из-за рассогласования при ``year=2023, month=11, day=10`` функция
    получает на вход ``day=2023, month=11, year=10`` и возвращает
    ``None``.

Эти тесты:
    1. Фиксируют наблюдаемое неверное поведение исходной функции
       (when called в порядке (year, month, day) — как было в коде запуска).
    2. Подтверждают, что исправленная версия даёт корректный результат
       на том же входе.
"""

from __future__ import annotations

from third_laboratory.services.nextday import next_day as fixed_next_day
from third_laboratory.services.nextday_legacy import (
    next_day as legacy_next_day,
)


class TestArgumentOrderBug:
    """Главный fault — путаница в порядке параметров."""

    def test_legacy_returns_none_when_called_with_year_first(self) -> None:
        # Сценарий из задания: пользователь ввёл год=2023, месяц=11, день=10.
        # Код запуска вызывает next_day(year, month, day), но исходная
        # функция ожидает (day, month, year) → получает (2023, 11, 10),
        # т.е. day=2023, и проверка day > max_days(11, 10) выходит True.
        assert legacy_next_day(2023, 11, 10) is None

    def test_fixed_returns_correct_date_for_same_inputs(self) -> None:
        # Та же тройка значений, но передана в порядке (year, month, day),
        # как и предполагалось в коде запуска.
        assert fixed_next_day(2023, 11, 10) == (2023, 11, 11)

    def test_legacy_works_only_when_invoked_correctly(self) -> None:
        # Если же звать legacy в её "родном" порядке (day, month, year),
        # она работает: 10.11.2023 → 11.11.2023 (в обратном порядке).
        assert legacy_next_day(10, 11, 2023) == (11, 11, 2023)
