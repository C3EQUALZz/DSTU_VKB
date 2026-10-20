"""Регрессия скидки: нормальные, дробные и граничные значения."""

import logging
from decimal import Decimal

import pytest

from fifth_laboratory import legacy
from fifth_laboratory.order import Item, Order, calculate_total


def make_order(discount: str = "10") -> Order:
    return Order("TEST-001", (Item("Keyboard", Decimal("1200"), 2), Item("Mouse", Decimal("1600"), 1)), Decimal(discount))


def test_discount_regression():
    # Именно этот тест запускается до и после исправления.
    assert calculate_total(make_order()) == Decimal("3600.00")


def test_legacy_reproduces_defect():
    assert legacy.calculate_total(make_order()) == Decimal("4000.00")


@pytest.mark.parametrize(("discount", "expected"), [
    ("0", "4000.00"), ("0.5", "3980.00"), ("10", "3600.00"),
    ("25", "3000.00"), ("100", "0.00"),
])
def test_discount_boundaries(discount, expected):
    assert calculate_total(make_order(discount)) == Decimal(expected)


def test_rounding_to_kopeck():
    order = Order("ROUND", (Item("Item", Decimal("0.05"), 1),), Decimal("10"))
    assert calculate_total(order) == Decimal("0.05")  # 0.045 -> 0.05


@pytest.mark.parametrize("discount", ["-1", "101", "NaN"])
def test_invalid_discount(discount):
    with pytest.raises(ValueError, match="Скидка"):
        make_order(discount)


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_invalid_quantity(quantity):
    with pytest.raises(ValueError, match="Количество"):
        Item("Item", Decimal("100"), quantity)


def test_trace_contains_intermediate_values(caplog):
    with caplog.at_level(logging.DEBUG, logger="lab5.order"):
        calculate_total(make_order())
    assert "subtotal=4000.00" in caplog.text
    assert "discount_percent=10 rate=0.1" in caplog.text
    assert "discount_amount=400.00 total=3600.00" in caplog.text
