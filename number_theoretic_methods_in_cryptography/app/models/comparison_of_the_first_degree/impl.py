"""
Сравнение первой степени
"""

from math import gcd
from typing import Final, Iterable
from typing import override

from app.core.registry import LogRegistry
from app.exceptions.models.congruence import NoSolutionSinceGCDDoesNotShareFreeTermError, ReverseElementWasNotFound
from app.models.comparison_of_the_first_degree.base import ILinearCongruenceSolver


class LinearCongruenceSolver(ILinearCongruenceSolver):
    def __init__(self) -> None:
        self._logger: Final[LogRegistry] = LogRegistry()

    @override
    def solve(self, coefficient: int, constant_term: int, modulus: int) -> int:
        """
        Решает сравнение первой степени: ax ≡ b (mod m)
        Возвращает:
            x: Основное решение
            None: Если решение не существует
        """
        # Шаг 1: Проверка существования решения
        gcd_value: int = gcd(coefficient, modulus)
        self._logger.add_log(f"НОД({coefficient}, {modulus}) = {gcd_value}")

        if constant_term % gcd_value != 0:
            raise NoSolutionSinceGCDDoesNotShareFreeTermError(
                "Решение не существует, так как НОД не делит свободный член."
            )

        # Шаг 2: Упрощение сравнения
        simplified_coefficient: int = coefficient // gcd_value
        simplified_constant: int = constant_term // gcd_value
        simplified_modulus: int = modulus // gcd_value
        self._logger.add_log(
            f"Упрощенное сравнение: {simplified_coefficient}x = {simplified_constant} (mod {simplified_modulus})"
        )

        # Шаг 3: Поиск обратного элемента
        inverse: int | None = self._find_modular_inverse(simplified_coefficient, simplified_modulus)
        if inverse is None:
            raise ReverseElementWasNotFound("Обратный элемент не найден.")

        self._logger.add_log(
            f"Обратный элемент {simplified_coefficient}⁻¹ по модулю {simplified_modulus} равен {inverse}"
        )

        # Шаг 4: Вычисление основного решения
        base_solution: int = (simplified_constant * inverse) % simplified_modulus
        self._logger.add_log(
            f"Основное решение: x = {base_solution} (mod {simplified_modulus})"
        )

        # Шаг 5: Все решения
        all_solutions: list[int] = [base_solution + k * simplified_modulus for k in range(gcd_value)]
        self._logger.add_log("Все решения:")

        for solution in all_solutions:
            self._logger.add_log(f"x = {solution} (mod {modulus})")

        return base_solution

    @staticmethod
    def _find_modular_inverse(number: int, modulus: int) -> int | None:
        """Находит обратный элемент числа number по модулю modulus"""
        original_modulus: int = modulus
        x0, x1 = 0, 1

        if modulus == 1:
            return None

        while number > 1:
            q: int = number // modulus
            number, modulus = modulus, number % modulus
            x0, x1 = x1 - q * x0, x0

        if x1 < 0:
            x1 += original_modulus

        return x1 if number == 1 else None

    @override
    def get_logs(self) -> Iterable[str]:
        return self._logger.logs
