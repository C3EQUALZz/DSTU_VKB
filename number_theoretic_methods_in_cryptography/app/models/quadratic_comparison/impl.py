import math
from typing import Final, Iterable, override

from app.core.registry import LogRegistry
from app.exceptions.models.qudratic_comparison import ModulusMustBeAnOddPrimeNumberError, NotAQuadraticDeductionError
from app.models.quadratic_comparison.base import IQuadraticComparisonModel


class QuadraticComparisonModel(IQuadraticComparisonModel):
    def __init__(self) -> None:
        self._registry: Final[LogRegistry] = LogRegistry()

    @override
    def solve_quadratic_comparison(
            self,
            number: int,
            prime: int
    ) -> tuple[int, int]:
        """Решает квадратичное сравнение x² ≡ number mod prime"""

        # Проверка входных данных
        if not self.__is_prime(prime) or prime == 2:
            raise ModulusMustBeAnOddPrimeNumberError("Модуль должен быть нечётным простым числом")

        # Проверка квадратичной вычетности
        legendre: int = self.__compute_legendre_symbol(number, prime)
        self._registry.add_log(f"Символ Лежандра ({number}/{prime}) = {legendre}")

        if legendre != 1:
            raise NotAQuadraticDeductionError(f"{number} не является квадратичным вычетом по модулю {prime}")

        # Поиск квадратичного невычета
        non_residue = self.__find_min_quadratic_non_residue(prime)
        self._registry.add_log(f"Минимальный квадратичный невычет: {non_residue}")

        roots: tuple[int, int] = self.__tonelli_shanks(number, prime, non_residue)
        max_root: int = max(roots)
        self._registry.add_log(f"Максимальный корень: {max_root}")
        return roots

    @override
    def get_logs(self) -> Iterable[str]:
        return self._registry.logs

    def __tonelli_shanks(
            self,
            number: int,
            prime: int,
            quadratic_nonresidue: int
    ) -> tuple[int, int]:
        """Вычисляет квадратные корни по алгоритму Тонелли-Шенкса"""
        self._registry.add_log(f"Алгоритм Тонелли-Шенкса для x² = {number} mod {prime}")

        # Проверка: number должен быть квадратичным вычетом
        legendre = self.__compute_legendre_symbol(number, prime)
        if legendre != 1:
            raise ValueError(f"{number} не является квадратичным вычетом по модулю {prime}")

        # Разложение prime-1 = odd_factor * 2^exponent
        odd_factor: int = prime - 1
        exponent: int = 0
        while odd_factor % 2 == 0:
            odd_factor //= 2
            exponent += 1

        self._registry.add_log(f"Разложение: {prime}-1 = {odd_factor} * 2^{exponent}")

        # Инициализация параметров
        current_exponent: int = exponent
        c_value: int = pow(quadratic_nonresidue, odd_factor, prime)
        t_value: int = pow(number, odd_factor, prime)
        root_candidate: int = pow(number, (odd_factor + 1) // 2, prime)

        self._registry.add_log(
            f"Инициализация: exponent={current_exponent}, "
            f"c={c_value}, t={t_value}, root={root_candidate}"
        )

        # Главный цикл алгоритма
        while t_value != 1:
            # Поиск минимального i: t^(2^i) ≡ 1
            min_exp = 0
            temp_t = t_value
            while temp_t != 1:
                temp_t = pow(temp_t, 2, prime)
                min_exp += 1

            self._registry.add_log(f"Найдено i={min_exp} (t^(2^{min_exp}) = 1)")

            # Вычисление корректирующего множителя
            shift: int = current_exponent - min_exp - 1
            b_value: int = pow(c_value, 1 << shift, prime)

            # Обновление параметров
            current_exponent: int = min_exp
            c_value: int = pow(b_value, 2, prime)
            t_value: int = (t_value * c_value) % prime
            root_candidate: int = (root_candidate * b_value) % prime

            self._registry.add_log(
                f"Обновление: exponent={current_exponent}, "
                f"c={c_value}, t={t_value}, root={root_candidate}"
            )

        root1: int = root_candidate
        root2: int = prime - root1
        self._registry.add_log(f"Найденные корни: {root1} и {root2}")
        return root1, root2



    def __find_min_quadratic_non_residue(self, prime: int) -> int:
        """Находит минимальный квадратичный невычет по модулю prime"""
        for candidate in range(2, prime):
            if self.__compute_legendre_symbol(candidate, prime) == prime - 1:  # -1 mod prime
                return candidate
        raise ValueError(f"Не найден квадратичный невычет для {prime}")

    def __compute_legendre_symbol(self, base: int, prime: int) -> int:
        """Вычисляет символ Лежандра (base/prime)"""
        # Символ Лежандра: a^((p-1)/2) mod p
        exponent: int = (prime - 1) // 2
        result: int = pow(base, exponent, prime)

        self._registry.add_log(
            f"Символ Лежандра ({base}/{prime}) = {result if result != prime - 1 else f'{result} (= -1)'}")
        return result

    @staticmethod
    def __is_prime(number: int) -> bool:
        """Проверяет, является ли число простым"""
        if number < 2:
            return False
        if number == 2:
            return True
        if number % 2 == 0:
            return False

        limit = math.isqrt(number)
        for divisor in range(3, limit + 1, 2):
            if number % divisor == 0:
                return False
        return True
