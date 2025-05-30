from copy import copy
from typing import Final, Iterable, override

from app.core.registry import LogRegistry
from app.models.legendre_and_jacobi_symbols.base import ILegendreJacobiModel


class LegendreJacobiModel(ILegendreJacobiModel):
    def __init__(self) -> None:
        self._legendre_registry: Final[LogRegistry] = LogRegistry()
        self._jacobi_registry: Final[LogRegistry] = LogRegistry()

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
        self._legendre_registry.add_log(
            f"Вычисление символа Лежандра для ({numerator}/{prime_denominator})"
        )

        if prime_denominator <= 1 or not self.__is_prime(prime_denominator):
            error_msg = "Знаменатель должен быть простым числом"
            self._legendre_registry.add_log(f"Ошибка: {error_msg}")
            return -2

        if numerator == 0 or numerator == 1:
            self._legendre_registry.add_log(
                f"Числитель равен {numerator}, возвращаем результат: {numerator}"
            )
            return numerator

        current_numerator: int = numerator % prime_denominator
        self._legendre_registry.add_log(
            f"Приводим числитель к модулю простого знаменателя: {current_numerator}"
        )

        exponent = (prime_denominator - 1) // 2
        self._legendre_registry.add_log(
            f"Вычисляем показатель степени e = (p-1)//2 = {exponent}"
        )

        result: int = pow(current_numerator, exponent, prime_denominator)
        self._legendre_registry.add_log(
            f"Вычисляем pow({current_numerator}, {exponent}, {prime_denominator}) = {result}"
        )

        if result == 1:
            self._legendre_registry.add_log("Результат = 1 (квадратичный вычет)")
            return 1
        elif result == prime_denominator - 1:
            self._legendre_registry.add_log("Результат = -1 (неквадратичный вычет)")
            return -1

        self._legendre_registry.add_log("Результат = 0 (числитель делится на знаменатель)")
        return 0

    @override
    def calculate_jacobi(self, numerator: int, denominator: int) -> int:
        """
        Вычисляет символ Якоби (a/n) по алгоритму, основанному на расширенном алгоритме Евклида.

        Args:
            numerator: Числитель символа Якоби (a)
            denominator: Знаменатель символа Якоби (n), должен быть положительным нечетным числом

        Returns:
            int: Символ Якоби (a/n), принимающий значения -1, 0 или 1

        Raises:
            ValueError: Если знаменатель не положителен или четен
        """
        self._jacobi_registry.add_log(f"Вычисление символа Якоби для ({numerator}/{denominator})")

        if denominator <= 0 or denominator % 2 == 0:
            raise ValueError("Знаменатель должен быть положительным нечетным числом")

        # Приведение числителя по модулю знаменателя
        current_numerator: int = numerator % denominator
        self._jacobi_registry.add_log(f"Приводим числитель к модулю знаменателя: a = {current_numerator}")

        if current_numerator == 0:
            self._jacobi_registry.add_log("Числитель = 0 mod знаменатель, результат: 0")
            return 0

        # Переменная для хранения знака результата
        result_sign: int = 1

        while current_numerator != 0:
            # Шаг 1: Удаление всех множителей 2 из числителя
            while current_numerator % 2 == 0:
                current_numerator //= 2
                mod8_remainder = denominator % 8

                if mod8_remainder in (3, 5):
                    result_sign *= -1

                self._jacobi_registry.add_log(
                    f"Числитель четное, делим на 2 -> a={current_numerator}, sign={result_sign}")

            # Шаг 2: Обмен числителя и знаменателя
            current_numerator, denominator = denominator, current_numerator
            self._jacobi_registry.add_log(
                f"Меняем местами числитель и знаменатель: a={current_numerator}, n={denominator}")

            # Шаг 3: Изменение знака при условии a ≡ n ≡ 3 mod 4
            if current_numerator % 4 == 3 and denominator % 4 == 3:
                result_sign *= -1
                self._jacobi_registry.add_log(f"a = 3 mod 4 и n = 3 mod 4 → изменение знака sign={result_sign}")

            # Шаг 4: Приведение числителя по модулю знаменателя
            current_numerator = current_numerator % denominator
            self._jacobi_registry.add_log(f"Приводим числитель к модулю знаменателя: a={current_numerator}")

        # Шаг 5: Проверка завершения алгоритма
        if denominator == 1:
            self._jacobi_registry.add_log(f"Знаменатель = 1, возвращаем результат: {result_sign}")
            return result_sign
        else:
            self._jacobi_registry.add_log(f"Знаменатель != 1, возвращаем результат: 0")
            return 0

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
    def get_legendre_logs(self) -> Iterable[str]:
        result: Iterable[str] = copy(self._legendre_registry.logs)
        self._legendre_registry.clear_logs()
        return result

    @override
    def get_jacobi_logs(self) -> Iterable[str]:
        result: Iterable[str] = copy(self._jacobi_registry.logs)
        self._jacobi_registry.clear_logs()
        return result
