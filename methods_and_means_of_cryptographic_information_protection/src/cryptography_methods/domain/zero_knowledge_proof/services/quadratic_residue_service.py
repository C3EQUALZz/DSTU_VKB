"""Сервис для работы с квадратичными вычетами."""
import logging
import secrets
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class QuadraticResidueService(DomainService):
    """Сервис для работы с квадратичными вычетами."""

    def __init__(self, modular_arithmetic_service: ModularArithmeticService) -> None:
        super().__init__()
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

    def legendre_symbol(self, a: int, p: int) -> int:
        """Вычисляет символ Лежандра (a/p).

        Args:
            a: Число
            p: Нечетное простое число

        Returns:
            Символ Лежандра: 1, -1 или 0
        """
        logger.debug(f"Computing Legendre symbol ({a}/{p})")
        result = self._modular_arithmetic.mod_pow(a, (p - 1) // 2, p)

        if result == p - 1:
            result = -1

        logger.debug(f"Legendre symbol ({a}/{p}) = {result}")
        return result

    def jacobi_symbol(self, a: int, n: int) -> int:
        """Вычисляет символ Якоби (a/n).

        Args:
            a: Число
            n: Положительное нечетное число

        Returns:
            Символ Якоби: 1, -1 или 0
        """
        if n <= 0 or n % 2 == 0:
            raise ValueError("n должно быть положительным нечетным числом")

        logger.debug(f"Computing Jacobi symbol ({a}/{n})")
        a = a % n
        t = 1

        while a != 0:
            while a % 2 == 0:
                a //= 2
                r = n % 8
                if r == 3 or r == 5:
                    t = -t

            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                t = -t

            a = a % n

        result = t if n == 1 else 0
        logger.debug(f"Jacobi symbol result: {result}")
        return result

    def is_quadratic_residue(self, a: int, p: int, q: int) -> bool:
        """Проверяет, является ли число квадратичным вычетом по модулю n = p * q.

        Args:
            a: Число для проверки
            p: Первое простое число
            q: Второе простое число

        Returns:
            True если число является квадратичным вычетом
        """
        logger.debug(f"Checking if {a} is quadratic residue mod {p}*{q}")
        jacobi_p = self.legendre_symbol(a, p)
        jacobi_q = self.legendre_symbol(a, q)
        result = jacobi_p == 1 and jacobi_q == 1
        logger.debug(f"Result: {result} (Jacobi({a}/{p})={jacobi_p}, Jacobi({a}/{q})={jacobi_q})")
        return result

    def find_random_quadratic_residue(self, n: int, p: int, q: int) -> int:
        """Находит случайный квадратичный вычет по модулю n = p * q.

        Args:
            n: Модуль (p * q)
            p: Первое простое число
            q: Второе простое число

        Returns:
            Случайный квадратичный вычет
        """
        logger.info(f"Finding random quadratic residue mod {n}")
        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            a = self._generate_random_in_range(1, n)
            logger.debug(f"Attempt {attempt + 1}: Testing {a}")

            if self.is_quadratic_residue(a, p, q):
                logger.info(f"Found quadratic residue: {a}")
                return a

            attempt += 1

        raise RuntimeError(f"Failed to find quadratic residue after {max_attempts} attempts")

    def tonelli_shanks(self, a: int, p: int) -> int | None:
        """Алгоритм Тонелли-Шенкса для нахождения квадратного корня по модулю простого числа.

        Args:
            a: Число
            p: Нечетное простое число

        Returns:
            Квадратный корень или None, если не существует
        """
        logger.debug(f"Tonelli-Shanks algorithm for sqrt({a}) mod {p}")

        if self.legendre_symbol(a, p) != 1:
            logger.warning(f"{a} is not a quadratic residue mod {p}")
            return None

        if p == 2:
            result = a % p
            logger.debug(f"p == 2, result: {result}")
            return result

        if p % 4 == 3:
            result = self._modular_arithmetic.mod_pow(a, (p + 1) // 4, p)
            logger.debug(f"p % 4 == 3, result: {result}")
            return result

        # p % 4 == 1
        q = p - 1
        s = 0
        while q % 2 == 0:
            q //= 2
            s += 1

        logger.debug(f"p - 1 = {q} * 2^{s}")

        z = 2
        while self.legendre_symbol(z, p) != -1:
            z += 1

        logger.debug(f"Found non-residue z = {z}")

        c = self._modular_arithmetic.mod_pow(z, q, p)
        x = self._modular_arithmetic.mod_pow(a, (q + 1) // 2, p)
        t = self._modular_arithmetic.mod_pow(a, q, p)
        m = s

        while t != 1:
            i = 0
            temp = t
            while temp != 1 and i < m:
                temp = self._modular_arithmetic.mod_pow(temp, 2, p)
                i += 1

            b = self._modular_arithmetic.mod_pow(c, 1 << (m - i - 1), p)
            x = (x * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i

            logger.debug(f"Loop: x = {x}, t = {t}, m = {m}")

        logger.debug(f"Square root: {x}")
        return x

    def find_square_root_mod_n(self, a: int, n: int, p: int, q: int) -> int | None:
        """Находит квадратный корень по модулю n = p * q используя китайскую теорему об остатках.

        Args:
            a: Число
            n: Модуль (p * q)
            p: Первое простое число
            q: Второе простое число

        Returns:
            Квадратный корень или None, если не существует
        """
        logger.debug(f"Finding square root of {a} mod {n} using CRT")
        sqrt_p = self.tonelli_shanks(a, p)
        sqrt_q = self.tonelli_shanks(a, q)

        if sqrt_p is None or sqrt_q is None:
            logger.warning(f"Square root does not exist mod {p} or mod {q}")
            return None

        logger.debug(f"sqrt({a}) mod {p} = {sqrt_p}, sqrt({a}) mod {q} = {sqrt_q}")

        inv_p = self._modular_arithmetic.mod_inverse(q, p)
        inv_q = self._modular_arithmetic.mod_inverse(p, q)

        if inv_p is None or inv_q is None:
            logger.error("Failed to compute modular inverses")
            return None

        logger.debug(f"inv({q}) mod {p} = {inv_p}, inv({p}) mod {q} = {inv_q}")

        # Китайская теорема об остатках
        result = (sqrt_p * q * inv_p + sqrt_q * p * inv_q) % n
        result = (result + n) % n

        logger.debug(f"Square root mod {n}: {result}")
        return result

    def _generate_random_in_range(self, min_value: int, max_value: int) -> int:
        """Генерирует случайное число в заданном диапазоне.

        Args:
            min_value: Минимальное значение (включительно)
            max_value: Максимальное значение (исключительно)

        Returns:
            Случайное число в диапазоне [min_value, max_value)
        """
        range_size = max_value - min_value
        num_bytes = (range_size.bit_length() + 7) // 8

        while True:
            random_bytes = secrets.token_bytes(num_bytes)
            candidate = int.from_bytes(random_bytes, byteorder='big')
            candidate = min_value + (candidate % range_size)

            if min_value <= candidate < max_value:
                return candidate


