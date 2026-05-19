"""Тесты-«пугалки» — фиксируют **наблюдаемые** дефекты исходной функции.

Назначение: продемонстрировать, что без исправлений код возвращает
неправильные ответы. Эти тесты НЕ являются регрессией функционала
— это «золотой стандарт» дефекта. Ожидаемое значение в assert — это
**фактическое (неверное)** поведение оригинальной функции; рядом в
комментарии — то, что *должно* было быть.

После исправления исходной функции (см. ``triangle.py``) эти тесты
показали бы тот самый failure, ради которого мы и поднимали тему.
"""

from __future__ import annotations

from second_laboratory.legacy import classify_triangle as legacy_classify
from second_laboratory.triangle import classify_triangle as fixed_classify


class TestLegacyDegenerateTriangleBug:
    """Главный fault: legacy игнорирует неравенство треугольника."""

    def test_77_14_legacy_returns_isosceles(self) -> None:
        # 7+7 == 14, реального треугольника нет, но legacy считает "Равнобедренный"
        assert legacy_classify(7, 7, 14) == "Равнобедренный"

    def test_77_14_fixed_returns_invalid(self) -> None:
        assert fixed_classify(7, 7, 14) == "InvalidInput"

    def test_1_2_10_legacy_classifies_as_scalene(self) -> None:
        # 1+2 < 10, треугольник невозможен, но legacy считает "Разносторонний"
        assert legacy_classify(1, 2, 10) == "Разносторонний"

    def test_1_2_10_fixed_returns_invalid(self) -> None:
        assert fixed_classify(1, 2, 10) == "InvalidInput"


class TestLegacyDocstringMismatch:
    """Второй fault: docstring обещает английские строки, возвращаются русские."""

    def test_equilateral_label_mismatch(self) -> None:
        assert legacy_classify(5, 5, 5) == "Равносторонний"   # docstring обещал "Equilateral"
        assert fixed_classify(5, 5, 5) == "Equilateral"

    def test_isosceles_label_mismatch(self) -> None:
        assert legacy_classify(5, 5, 3) == "Равнобедренный"   # docstring обещал "Isosceles"
        assert fixed_classify(5, 5, 3) == "Isosceles"

    def test_scalene_label_mismatch(self) -> None:
        assert legacy_classify(3, 4, 5) == "Разносторонний"   # docstring обещал "Scalene"
        assert fixed_classify(3, 4, 5) == "Scalene"


class TestLegacyBoolBug:
    """Третий fault: bool — подкласс int, legacy пропускает (True, True, True)."""

    def test_bool_accepted_by_legacy(self) -> None:
        assert legacy_classify(True, True, True) == "Равносторонний"

    def test_bool_rejected_by_fixed(self) -> None:
        assert fixed_classify(True, True, True) == "InvalidInput"
