"""CLI: python -m fifth_laboratory --version legacy|fixed --check."""

import argparse
import json
import logging
from decimal import Decimal
from pathlib import Path

from . import legacy
from .order import Item, Order, calculate_total


def configure_logging(level: str, log_file: Path | None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, mode="w", encoding="utf-8"))
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
        force=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Расчёт заказа: трассировка через logging")
    parser.add_argument("--input", type=Path, default=Path("data/order.json"))
    parser.add_argument("--version", choices=("legacy", "fixed"), default="fixed")
    parser.add_argument("--log-level", choices=("DEBUG", "INFO", "WARNING", "ERROR"), default="INFO")
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--check", action="store_true", help="Сравнить с expected_total из JSON")
    args = parser.parse_args()
    configure_logging(args.log_level, args.log_file)
    logger = logging.getLogger("lab5.cli")
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"), parse_float=Decimal)
        order = Order(
            order_id=data["order_id"],
            items=tuple(Item(i["name"], Decimal(i["price"]), i["quantity"]) for i in data["items"]),
            discount_percent=Decimal(data["discount_percent"]),
        )
        calculator = legacy.calculate_total if args.version == "legacy" else calculate_total
        logger.info("version=%s", args.version)
        total = calculator(order)
        print(f"Order: {order.order_id} | version: {args.version}", flush=True)
        print(f"Total: {total:.2f} RUB", flush=True)
        if args.check:
            expected = Decimal(data["expected_total"])
            if total != expected:
                logger.error("CHECK FAILED expected=%.2f actual=%.2f delta=%.2f", expected, total, total - expected)
                print(f"CHECK: FAIL (expected {expected:.2f})", flush=True)
                return 1
            logger.info("CHECK PASSED expected=%.2f actual=%.2f", expected, total)
            print("CHECK: PASS", flush=True)
        return 0
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError):
        logger.exception("Не удалось обработать заказ")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
