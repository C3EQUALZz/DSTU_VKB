"""Одинаковый сценарий для pdb, PyCharm и обычного запуска."""

import argparse

from average import average
from average_legacy import average as legacy_average


def main() -> int:
    parser = argparse.ArgumentParser(description="Лабораторная №6: отладка среднего")
    parser.add_argument("--version", choices=("legacy", "fixed"), default="legacy")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    values = [10, 20, 30, 40]
    expected = 25.0
    calculator = legacy_average if args.version == "legacy" else average
    result = calculator(values)
    print(f"Version: {args.version}")
    print(f"Values: {values}")
    print(f"Average: {result:.2f}; expected: {expected:.2f}")
    if args.check:
        passed = result == expected
        print("CHECK: PASS" if passed else "CHECK: FAIL")
        return 0 if passed else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
