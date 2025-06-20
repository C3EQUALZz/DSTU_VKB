"""
Вычислить значения величины S, которая задана следующим образом:

S = Sum(Prod(sin(pi * i / k))

Натурально число N вводится с клавиатуры, причем N > 2
"""

import math
from functools import reduce
from operator import mul


def main() -> None:
    n: int = int(input("Введите натуральное число N (N > 2): "))

    if n <= 2:
        print("Ошибка: N должно быть больше 2")
        return

    total_sum: float = 0.0

    # Внешний цикл: сумма по k от 2 до N
    for k in range(2, n + 1):
        # Создаем список значений синуса для i = 1..k-1
        terms = (math.sin(math.pi * i / k) for i in range(1, k))

        # Вычисляем произведение с помощью reduce
        product: float = reduce(mul, terms, 1.0)

        total_sum += product

    print(f"S = {total_sum:.6f}")


if __name__ == "__main__":
    main()
