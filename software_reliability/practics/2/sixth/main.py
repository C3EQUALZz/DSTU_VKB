"""
Вычислить переменную S, которая задана следующим образом:

S = Σ (-1)^k * (2k + 1)!

Натуральное число N вводится с клавиатуры. Результат вывести на экран.
"""
import math


def calculate_s(n_terms: int) -> float:
    total: float = 0
    for k in range(1, n_terms + 1):
        num: int = 2 * k + 1
        fact: float = math.factorial(num)
        sign: int = -1 if k % 2 == 1 else 1
        total += sign * fact
    return total


def main() -> None:
    n: int = int(input("Введите натуральное число N: "))
    if n < 1:
        raise ValueError("N должно быть натуральным числом (≥1)")
    result: float = calculate_s(n)
    print(f"Сумма S = {result}")


if __name__ == "__main__":
    main()
