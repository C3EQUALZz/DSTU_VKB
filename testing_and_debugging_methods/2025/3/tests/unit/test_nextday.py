"""Тесты `next_day` по разбиению входных значений на эквивалентные классы.

ЭКВИВАЛЕНТНЫЕ КЛАССЫ
====================

Year (Y) — валидные:
    Y1  : невисокосный год              (например 2023, 1900, 2100)
    Y2  : високосный, кратный 4 не 100  (например 2024, 2020)
    Y3  : високосный, кратный 400       (например 2000, 2400)
Year — невалидные:
    Y4  : year < 1                       (0, -1)
    Y5  : not int                        (None, "2023", 2023.0, True)

Month (M) — валидные:
    M1  : месяц с 31 днём                {1, 3, 5, 7, 8, 10, 12}
    M2  : месяц с 30 днями               {4, 6, 9, 11}
    M3  : февраль                        {2}
Month — невалидные:
    M4  : month < 1                      (0, -1)
    M5  : month > 12                     (13, 100)
    M6  : not int

Day (D) — валидные:
    D1  : обычный день (не последний)   1 .. max_days-1
    D2  : последний день не-декабря     {28|29 февраль, 30 апреля, 31 января ...}
    D3  : последний день декабря        31 декабря
Day — невалидные:
    D4  : day < 1                        (0, -5)
    D5  : day > days_in_month            (32, 30 февраля)
    D6  : not int
"""

from __future__ import annotations

import pytest

from third_laboratory.services.nextday import (
    days_in_month,
    is_leap_year,
    next_day,
)


# ============================================================================
# Вспомогательные функции (тестируем как побочный продукт next_day)
# ============================================================================

class TestIsLeapYear:
    """Y1, Y2, Y3 на уровне вспомогательной функции."""

    @pytest.mark.parametrize("year", [2023, 1900, 2100, 1, 2025])
    def test_non_leap_year(self, year: int) -> None:
        assert is_leap_year(year) is False

    @pytest.mark.parametrize("year", [2024, 2020, 4, 1996])
    def test_leap_year_div_by_4_not_100(self, year: int) -> None:
        assert is_leap_year(year) is True

    @pytest.mark.parametrize("year", [2000, 2400, 400, 1600])
    def test_leap_year_div_by_400(self, year: int) -> None:
        assert is_leap_year(year) is True


class TestDaysInMonth:
    """M1, M2, M3 + сочетание M3 с Y1/Y2/Y3."""

    @pytest.mark.parametrize("month", [1, 3, 5, 7, 8, 10, 12])
    def test_31_day_months(self, month: int) -> None:
        assert days_in_month(month, 2023) == 31

    @pytest.mark.parametrize("month", [4, 6, 9, 11])
    def test_30_day_months(self, month: int) -> None:
        assert days_in_month(month, 2023) == 30

    def test_february_non_leap(self) -> None:
        assert days_in_month(2, 2023) == 28

    def test_february_leap_div4(self) -> None:
        assert days_in_month(2, 2024) == 29

    def test_february_century_non_leap(self) -> None:
        # Y1: 1900 кратен 100, но не 400 → не високосный
        assert days_in_month(2, 1900) == 28

    def test_february_leap_div400(self) -> None:
        assert days_in_month(2, 2000) == 29

    @pytest.mark.parametrize("month", [0, -1, 13, 100])
    def test_invalid_month_returns_none(self, month: int) -> None:
        assert days_in_month(month, 2023) is None


# ============================================================================
# Задание №2: основные эквивалентные классы для next_day
# ============================================================================

class TestEquivalenceValidDay:
    """D1 / D2 / D3 — три валидных класса по дню."""

    def test_d1_ordinary_day(self) -> None:
        # D1 × M1 × Y1: обычный день
        assert next_day(2023, 1, 15) == (2023, 1, 16)

    def test_d2_last_day_of_non_december(self) -> None:
        # D2 × M1 × Y1: 31 января → 1 февраля
        assert next_day(2023, 1, 31) == (2023, 2, 1)

    def test_d3_last_day_of_december(self) -> None:
        # D3 × M1 × Y1: 31 декабря → 1 января следующего года
        assert next_day(2023, 12, 31) == (2024, 1, 1)


class TestEquivalenceValidMonth:
    """M1 / M2 / M3 — три валидных класса по месяцу."""

    @pytest.mark.parametrize(
        ("year", "month", "day", "expected"),
        [
            (2023, 1, 31, (2023, 2, 1)),     # M1: январь 31 → февраль 1
            (2023, 3, 31, (2023, 4, 1)),     # M1: март 31 → апрель 1
            (2023, 12, 31, (2024, 1, 1)),    # M1: декабрь 31 → след. год
        ],
    )
    def test_m1_31_day_months(
        self, year: int, month: int, day: int, expected: tuple
    ) -> None:
        assert next_day(year, month, day) == expected

    @pytest.mark.parametrize(
        ("year", "month", "day", "expected"),
        [
            (2023, 4, 30, (2023, 5, 1)),     # M2: апрель 30 → май 1
            (2023, 11, 30, (2023, 12, 1)),   # M2: ноябрь 30 → декабрь 1
        ],
    )
    def test_m2_30_day_months(
        self, year: int, month: int, day: int, expected: tuple
    ) -> None:
        assert next_day(year, month, day) == expected

    def test_m3_february_non_leap(self) -> None:
        # M3 × Y1: 28 февраля 2023 → 1 марта 2023
        assert next_day(2023, 2, 28) == (2023, 3, 1)

    def test_m3_february_leap(self) -> None:
        # M3 × Y2: 28 февраля 2024 → 29 февраля 2024
        assert next_day(2024, 2, 28) == (2024, 2, 29)
        # 29 февраля 2024 → 1 марта 2024
        assert next_day(2024, 2, 29) == (2024, 3, 1)


class TestEquivalenceValidYear:
    """Y1 / Y2 / Y3 — три валидных класса по году."""

    def test_y1_non_leap_year(self) -> None:
        # Y1: 28 февраля 2023 → 1 марта
        assert next_day(2023, 2, 28) == (2023, 3, 1)

    def test_y2_leap_year_div4(self) -> None:
        # Y2: 28 февраля 2024 → 29 февраля
        assert next_day(2024, 2, 28) == (2024, 2, 29)

    def test_y3_leap_year_div400(self) -> None:
        # Y3: 29 февраля 2000 → 1 марта
        assert next_day(2000, 2, 29) == (2000, 3, 1)

    def test_y1_century_non_leap(self) -> None:
        # Y1: 1900 кратен 100, но не 400 — невисокосный
        assert next_day(1900, 2, 28) == (1900, 3, 1)
        assert next_day(1900, 2, 29) is None


# ============================================================================
# Свойства: rollover (переход) дня → месяца → года
# ============================================================================

class TestMonthRollover:
    """D2: последний день не-декабря → 1 следующего месяца."""

    @pytest.mark.parametrize(
        ("year", "month", "last_day"),
        [
            (2023, 1, 31), (2023, 3, 31), (2023, 5, 31),
            (2023, 7, 31), (2023, 8, 31), (2023, 10, 31),
            (2023, 4, 30), (2023, 6, 30), (2023, 9, 30), (2023, 11, 30),
            (2023, 2, 28),     # февраль не високосного
            (2024, 2, 29),     # февраль високосного
        ],
    )
    def test_last_day_of_month_rolls_over(
        self, year: int, month: int, last_day: int
    ) -> None:
        result = next_day(year, month, last_day)
        assert result == (year, month + 1, 1)


class TestYearRollover:
    """D3: 31 декабря любого года → 1 января следующего."""

    @pytest.mark.parametrize("year", [1, 1999, 2000, 2023, 2024, 2400])
    def test_december_31_rolls_to_next_year(self, year: int) -> None:
        assert next_day(year, 12, 31) == (year + 1, 1, 1)


# ============================================================================
# Невалидные эквивалентные классы (Robust ECT)
# ============================================================================

class TestInvalidType:
    """Y5 / M6 / D6 — невалидный тип."""

    @pytest.mark.parametrize(
        ("year", "month", "day"),
        [
            ("2023", 11, 10),
            (2023, "11", 10),
            (2023, 11, "10"),
            (None, 11, 10),
            (2023, None, 10),
            (2023, 11, None),
            (2023.0, 11, 10),
            (2023, 11, 10.0),
            ([2023], 11, 10),
        ],
    )
    def test_non_int_returns_none(self, year, month, day) -> None:
        assert next_day(year, month, day) is None

    @pytest.mark.parametrize(
        ("year", "month", "day"),
        [
            (True, 1, 1),
            (2023, True, 1),
            (2023, 1, True),
            (False, 1, 1),
        ],
    )
    def test_bool_is_rejected(self, year, month, day) -> None:
        # bool — подкласс int в Python, но не должен считаться валидным.
        assert next_day(year, month, day) is None


class TestInvalidYear:
    """Y4: year < 1."""

    @pytest.mark.parametrize("year", [0, -1, -100, -2024])
    def test_year_less_than_1_returns_none(self, year: int) -> None:
        assert next_day(year, 1, 1) is None


class TestInvalidMonth:
    """M4, M5: month < 1 или > 12."""

    @pytest.mark.parametrize("month", [0, -1, -12])
    def test_month_less_than_1(self, month: int) -> None:
        assert next_day(2023, month, 15) is None

    @pytest.mark.parametrize("month", [13, 14, 100])
    def test_month_greater_than_12(self, month: int) -> None:
        assert next_day(2023, month, 15) is None


class TestInvalidDay:
    """D4, D5: day вне допустимого диапазона."""

    @pytest.mark.parametrize("day", [0, -1, -31])
    def test_day_less_than_1(self, day: int) -> None:
        assert next_day(2023, 1, day) is None

    @pytest.mark.parametrize(
        ("year", "month", "day"),
        [
            (2023, 1, 32),      # январь: max 31
            (2023, 4, 31),      # апрель: max 30
            (2023, 2, 29),      # февраль 2023 (не високосный): max 28
            (2023, 2, 30),
            (2024, 2, 30),      # февраль 2024 (високосный): max 29
            (2023, 12, 100),
        ],
    )
    def test_day_greater_than_max_days(
        self, year: int, month: int, day: int
    ) -> None:
        assert next_day(year, month, day) is None


# ============================================================================
# Граничные тест-кейсы по эквивалентным классам
# ============================================================================

class TestBoundary:
    """Граничные значения внутри каждого валидного класса."""

    def test_minimal_valid_date(self) -> None:
        # year=1, month=1, day=1: минимально допустимая дата
        assert next_day(1, 1, 1) == (1, 1, 2)

    def test_large_year(self) -> None:
        # Большое значение года
        assert next_day(99999, 1, 1) == (99999, 1, 2)

    def test_day_1_in_every_month(self) -> None:
        # День 1 в каждом месяце → день 2 того же месяца
        for month in range(1, 13):
            assert next_day(2023, month, 1) == (2023, month, 2)

    @pytest.mark.parametrize(
        ("year", "month", "day", "expected"),
        [
            # Полная карта смены месяца/года в 2024 (високосный)
            (2024, 1, 31, (2024, 2, 1)),
            (2024, 2, 28, (2024, 2, 29)),
            (2024, 2, 29, (2024, 3, 1)),
            (2024, 3, 31, (2024, 4, 1)),
            (2024, 4, 30, (2024, 5, 1)),
            (2024, 5, 31, (2024, 6, 1)),
            (2024, 6, 30, (2024, 7, 1)),
            (2024, 7, 31, (2024, 8, 1)),
            (2024, 8, 31, (2024, 9, 1)),
            (2024, 9, 30, (2024, 10, 1)),
            (2024, 10, 31, (2024, 11, 1)),
            (2024, 11, 30, (2024, 12, 1)),
            (2024, 12, 31, (2025, 1, 1)),
        ],
    )
    def test_full_calendar_year_rollovers_leap(
        self, year: int, month: int, day: int, expected: tuple
    ) -> None:
        assert next_day(year, month, day) == expected
