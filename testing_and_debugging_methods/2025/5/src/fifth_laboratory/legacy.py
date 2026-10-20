"""Исходная версия с дефектом. Сохранена для воспроизведения ошибки."""

from decimal import Decimal

from .order import Order, apply_discount, logger, subtotal


def calculate_total(order: Order) -> Decimal:
    logger.info("order=%s discount_percent=%s", order.order_id, order.discount_percent)
    amount = subtotal(order)
    # Дефект: int отбрасывает дробную часть коэффициента скидки.
    rate = Decimal(int(order.discount_percent / Decimal("100")))
    logger.debug("discount_percent=%s rate=%s", order.discount_percent, rate)
    return apply_discount(amount, rate)
