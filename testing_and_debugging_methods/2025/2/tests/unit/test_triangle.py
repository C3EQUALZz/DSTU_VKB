"""Полный набор тест-кейсов для исправленной classify_triangle.

Тесты сгруппированы в классы по характеру входных данных:
    - TestEquilateral          — равносторонние треугольники
    - TestIsosceles            — равнобедренные (две стороны равны)
    - TestScalene              — разносторонние (все стороны разные)
    - TestInvalidType          — невалидный тип параметров
    - TestNonPositive          — нулевые / отрицательные стороны
    - TestTriangleInequality   — нарушение неравенства треугольника
    - TestArgumentOrderInvariance — независимость результата от порядка
    - TestBoundary             — граничные значения
"""

from __future__ import annotations

import pytest

from second_laboratory.triangle import classify_triangle


class TestEquilateral:
    """Все три стороны равны → "Equilateral"."""

    @pytest.mark.parametrize("side", [1, 2, 3, 5, 10, 100, 1_000_000])
    def test_equal_sides(self, side: int) -> None:
        assert classify_triangle(side, side, side) == "Equilateral"

    def test_minimum_equilateral(self) -> None:
        # (1,1,1) — минимальный допустимый равносторонний
        assert classify_triangle(1, 1, 1) == "Equilateral"


class TestIsosceles:
    """Ровно две стороны равны и неравенство треугольника выполнено."""

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (5, 5, 3),   # a == b
            (3, 5, 5),   # b == c
            (5, 3, 5),   # a == c
            (2, 2, 3),
            (10, 10, 5),
            (100, 100, 50),
        ],
    )
    def test_two_equal_sides(self, a: int, b: int, c: int) -> None:
        assert classify_triangle(a, b, c) == "Isosceles"


class TestScalene:
    """Все три стороны разные и неравенство треугольника выполнено."""

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (3, 4, 5),       # классическая египетская тройка
            (5, 12, 13),
            (6, 8, 10),
            (7, 8, 9),
            (10, 14, 20),
        ],
    )
    def test_three_distinct_sides(self, a: int, b: int, c: int) -> None:
        assert classify_triangle(a, b, c) == "Scalene"


class TestInvalidType:
    """Нечисловые / float / bool значения — невалидный ввод."""

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            ("3", "4", "5"),         # строки
            (3.0, 4.0, 5.0),         # float
            (3, 4, 5.0),             # смешанные int/float
            (None, 4, 5),
            ([3], 4, 5),
            (object(), 4, 5),
        ],
    )
    def test_non_int_inputs(self, a, b, c) -> None:
        assert classify_triangle(a, b, c) == "InvalidInput"

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (True, True, True),       # bool — формально подкласс int
            (False, False, False),
            (1, 1, True),
        ],
    )
    def test_bool_is_rejected(self, a, b, c) -> None:
        # bool — это subclass int в Python; явно отвергаем как длину стороны.
        assert classify_triangle(a, b, c) == "InvalidInput"


class TestNonPositive:
    """Нулевые и отрицательные стороны — невалидный ввод."""

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (0, 0, 0),
            (0, 5, 5),
            (5, 0, 5),
            (5, 5, 0),
            (-1, 2, 3),
            (3, -2, 4),
            (3, 4, -5),
            (-3, -4, -5),
        ],
    )
    def test_zero_or_negative(self, a: int, b: int, c: int) -> None:
        assert classify_triangle(a, b, c) == "InvalidInput"


class TestTriangleInequality:
    """Нарушение неравенства треугольника a + b > c (по всем перестановкам)."""

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (7, 7, 14),    # вырожденный (равенство) — из задания
            (1, 2, 3),     # 1 + 2 == 3
            (5, 5, 10),
            (10, 1, 1),
        ],
    )
    def test_degenerate_triangle(self, a: int, b: int, c: int) -> None:
        """a + b == c (или симметрично) — стороны лежат на одной прямой."""
        assert classify_triangle(a, b, c) == "InvalidInput"

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (1, 2, 10),    # 1 + 2 < 10
            (3, 4, 100),
            (100, 1, 1),
            (1, 100, 1),
            (50, 50, 200),
        ],
    )
    def test_strict_inequality_violation(self, a: int, b: int, c: int) -> None:
        """a + b < c — треугольника не существует."""
        assert classify_triangle(a, b, c) == "InvalidInput"

    def test_minimal_valid_triangle(self) -> None:
        # (2,2,3): 2+2=4 > 3, 2+3=5 > 2, 2+3=5 > 2 — валидный isosceles
        assert classify_triangle(2, 2, 3) == "Isosceles"

    def test_just_above_degeneracy(self) -> None:
        # (5, 5, 9): 5+5=10 > 9 — на 1 больше предела
        assert classify_triangle(5, 5, 9) == "Isosceles"


class TestArgumentOrderInvariance:
    """Перестановка сторон не должна менять результат классификации."""

    @pytest.mark.parametrize(
        "sides",
        [(3, 4, 5), (5, 5, 8), (7, 7, 7), (1, 2, 3), (0, 1, 1)],
    )
    def test_all_permutations_equal(self, sides: tuple[int, int, int]) -> None:
        from itertools import permutations

        results = {classify_triangle(*p) for p in permutations(sides)}
        assert len(results) == 1, (
            f"Результаты разнятся для перестановок {sides}: {results}"
        )


class TestBoundary:
    """Граничные случаи: минимальные стороны, очень большие числа."""

    def test_smallest_possible(self) -> None:
        assert classify_triangle(1, 1, 1) == "Equilateral"

    def test_large_equilateral(self) -> None:
        assert classify_triangle(10**9, 10**9, 10**9) == "Equilateral"

    def test_large_scalene(self) -> None:
        assert classify_triangle(10**9, 10**9 + 1, 10**9 + 2) == "Scalene"

    @pytest.mark.parametrize(
        ("a", "b", "c", "expected"),
        [
            (2, 3, 4, "Scalene"),
            (4, 4, 4, "Equilateral"),
            (4, 4, 7, "Isosceles"),
            (1, 1, 2, "InvalidInput"),     # вырожденный
            (1, 1, 3, "InvalidInput"),     # не треугольник
        ],
    )
    def test_smoke_table(
        self, a: int, b: int, c: int, expected: str
    ) -> None:
        assert classify_triangle(a, b, c) == expected
