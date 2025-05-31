"""
Задание. Найти символ Лежандра (n / p). Написать программу, реализующую поиск символа Лежандра.
Для заданий лабораторной работы N – номер варианта, который указывается преподавателем.
Значения n, p находятся, как описано в pdf файле.
"""

from typing import override, Final, Iterable

from app.core.registry import LogRegistry
from app.exceptions.models.legendre_symbol import NumberMustBePrime
from app.models.legendre_symbol.base import ILegendreModel


class LegendreModel(ILegendreModel):
    def __init__(self) -> None:
        self._registry: Final[LogRegistry] = LogRegistry()

    @override
    def calculate_legendre(self, numerator: int, prime_denominator: int) -> int:
        """
        Вычисляет символ Лежандра (a|p) для целого числа a и простого числа p.

        Символ Лежандра определяется как:
            - 0, если a ≡ 0 mod p
            - 1, если a — квадратичный вычет по модулю p
            - -1, если a — неквадратичный вычет по модулю p

        Args:
            numerator: Числитель символа Лежандра
            prime_denominator: Простое число — знаменатель символа Лежандра

        Returns:
            int: Символ Лежандра (a|p), принимающий значения -1, 0 или 1
        """
        self._registry.add_log(
            f"Вычисление символа Лежандра для ({numerator}/{prime_denominator})"
        )

        if prime_denominator <= 1 or not self.__is_prime(prime_denominator):
            raise NumberMustBePrime(f"Ошибка: Знаменатель должен быть простым числом")

        if numerator == 0 or numerator == 1:
            self._registry.add_log(
                f"Числитель равен {numerator}, возвращаем результат: {numerator}"
            )
            return numerator

        current_numerator: int = numerator % prime_denominator
        self._registry.add_log(
            f"Приводим числитель к модулю простого знаменателя: {current_numerator}"
        )

        exponent = (prime_denominator - 1) // 2
        self._registry.add_log(
            f"Вычисляем показатель степени e = (p-1)//2 = {exponent}"
        )

        result: int = pow(current_numerator, exponent, prime_denominator)
        self._registry.add_log(
            f"Вычисляем pow({current_numerator}, {exponent}, {prime_denominator}) = {result}"
        )

        if result == 1:
            self._registry.add_log("Результат = 1 (квадратичный вычет)")
            return 1
        elif result == prime_denominator - 1:
            self._registry.add_log("Результат = -1 (неквадратичный вычет)")
            return -1

        self._registry.add_log("Результат = 0 (числитель делится на знаменатель)")
        return 0

    def generate_n_p(self, variant_number: int) -> tuple[int, int]:
        """
        Генерирует n и p по варианту
        """
        # Определение p
        p_cases: dict[int, int] = {
            0: 937,
            1: 941,
            2: 947,
            3: 953,
            4: 967
        }

        remainder: int = variant_number % 5
        p: int = p_cases[remainder]

        # Определение n
        if variant_number < 10:
            n = 30 * variant_number + 7
        else:
            n = 15 * variant_number - 11

        return n, p

    @staticmethod
    def __is_prime(n: int) -> bool:
        """Проверяет, является ли число простым."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @override
    def get_logs(self) -> Iterable[str]:
        return self._registry.logs
