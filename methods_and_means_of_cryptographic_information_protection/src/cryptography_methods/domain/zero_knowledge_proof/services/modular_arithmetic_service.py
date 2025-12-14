"""Сервис для работы с модульной арифметикой."""
import logging
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ModularArithmeticService(DomainService):
    """Сервис для выполнения операций модульной арифметики."""

    def __init__(self) -> None:
        super().__init__()

    def mod_pow(self, base: int, exponent: int, modulus: int) -> int:
        """Выполняет модульное возведение в степень: base^exponent mod modulus.

        Args:
            base: Основание
            exponent: Показатель степени
            modulus: Модуль

        Returns:
            Результат модульного возведения в степень
        """
        logger.debug(f"Computing {base}^{exponent} mod {modulus}")
        result = 1
        base = base % modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent >>= 1

        logger.debug(f"Result: {result}")
        return result

    def extended_euclidean(self, a: int, b: int) -> tuple[int, int, int]:
        """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов.

        Args:
            a: Первое число
            b: Второе число

        Returns:
            Кортеж (gcd, x, y) где gcd = НОД(a, b) и gcd = a*x + b*y
        """
        logger.debug(f"Extended Euclidean algorithm for {a} and {b}")
        if b == 0:
            gcd, x, y = a, 1, 0
            logger.debug(f"GCD: {gcd}, x: {x}, y: {y}")
            return gcd, x, y

        gcd, x1, y1 = self.extended_euclidean(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        logger.debug(f"GCD: {gcd}, x: {x}, y: {y}")
        return gcd, x, y

    def mod_inverse(self, a: int, modulus: int) -> int | None:
        """Находит модульный обратный элемент: a^(-1) mod modulus.

        Args:
            a: Число
            modulus: Модуль

        Returns:
            Модульный обратный элемент или None, если не существует
        """
        logger.debug(f"Finding modular inverse of {a} mod {modulus}")
        gcd, x, _ = self.extended_euclidean(a, modulus)

        if gcd != 1:
            logger.warning(f"Modular inverse does not exist: GCD({a}, {modulus}) = {gcd}")
            return None

        result = (x % modulus + modulus) % modulus
        logger.debug(f"Modular inverse: {result}")
        return result
