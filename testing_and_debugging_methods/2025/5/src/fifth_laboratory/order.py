"""Расчёт стоимости заказа и трассировка промежуточных значений."""

import logging
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

logger = logging.getLogger("lab5.order")
CENT = Decimal("0.01")


@dataclass(frozen=True)
class Item:
    name: str
    price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if not self.price.is_finite() or self.price < 0:
            raise ValueError("Цена должна быть конечной и неотрицательной")
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ValueError("Количество должно быть целым положительным числом")


@dataclass(frozen=True)
class Order:
    order_id: str
    items: tuple[Item, ...]
    discount_percent: Decimal

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Заказ должен содержать хотя бы одну позицию")
        if not self.discount_percent.is_finite() or not 0 <= self.discount_percent <= 100:
            raise ValueError("Скидка должна быть в диапазоне от 0 до 100 процентов")


def subtotal(order: Order) -> Decimal:
    total = Decimal("0")
    for item in order.items:
        line_total = item.price * item.quantity
        logger.debug(
            "item=%s price=%s qty=%d line_total=%.2f",
            item.name, item.price, item.quantity, line_total,
        )
        total += line_total
    logger.debug("subtotal=%.2f", total)
    return total


def apply_discount(amount: Decimal, rate: Decimal) -> Decimal:
    discount = amount * rate
    total = (amount - discount).quantize(CENT, rounding=ROUND_HALF_UP)
    logger.debug("discount_amount=%.2f total=%.2f", discount, total)
    return total


def calculate_total(order: Order) -> Decimal:
    """Исправленная версия: сохраняет дробную часть коэффициента скидки."""
    logger.info("order=%s discount_percent=%s", order.order_id, order.discount_percent)
    amount = subtotal(order)
    rate = order.discount_percent / Decimal("100")
    logger.debug("discount_percent=%s rate=%s", order.discount_percent, rate)
    return apply_discount(amount, rate)
