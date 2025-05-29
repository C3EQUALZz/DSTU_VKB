import math
from typing import Iterable, Final

from app.core.registry import LogRegistry
from app.exceptions.models.remainder_division import TheoremsCannotBeApplied
from app.models.remainder_division.base import IRemainderDivision


class EulerFermatModel(IRemainderDivision):
    def __init__(self) -> None:
        self._registry: Final[LogRegistry] = LogRegistry()

    def solve(self, a: int, exponent: int, modulus: int) -> int | None:
        """
        Вычисляет a^exponent % modulus с использованием теоремы Эйлера или Ферма.
        Возвращает результат и лог вычислений.
        """

        # Проверка, что a и modulus взаимно просты
        if math.gcd(a, modulus) != 1:
            raise TheoremsCannotBeApplied("Ошибка: a и модуль не взаимно просты. Теоремы не применимы.")

        # Проверка, является ли модуль простым (для малой теоремы Ферма)
        is_prime = self._is_prime(modulus)
        self._registry.add_log(f"Модуль {modulus} {'простой' if is_prime else 'составной'}")

        if is_prime:
            # Малая теорема Ферма: a^(p-1) ≡ 1 mod p
            reduced_exponent = exponent % (modulus - 1)
            self._registry.add_log(f"Малая теорема Ферма: уменьшаем степень {exponent} до {reduced_exponent}")
        else:
            # Теорема Эйлера: a^φ(n) ≡ 1 mod n
            phi = self._euler_phi(modulus)
            reduced_exponent = exponent % phi
            self._registry.add_log(f"Теорема Эйлера: уменьшаем степень {exponent} до {reduced_exponent}")

        # Вычисляем результат
        result = self._modular_pow(a, reduced_exponent, modulus)
        self._registry.add_log(f"Итоговое значение: {result}")

        return result

    @staticmethod
    def _is_prime(n: int) -> bool:
        """Проверяет, является ли число простым"""
        if n < 2:
            return False

        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False

        return True

    def _euler_phi(self, n: int) -> int:
        """Вычисляет функцию Эйлера φ(n)"""
        result = n
        i = 2
        temp_n = n
        self._registry.add_log(f"φ({n}) = {n}")

        while i * i <= temp_n:
            if temp_n % i == 0:
                self._registry.add_log(f"Найден множитель: {i}")
                while temp_n % i == 0:
                    temp_n //= i
                result -= result // i
                self._registry.add_log(f"φ(n) = {result}")
            i += 1

        if temp_n > 1:
            self._registry.add_log(f"Остаточный множитель: {temp_n}")
            result -= result // temp_n
            self._registry.add_log(f"φ(n) = {result}")

        return result

    def _modular_pow(self, base: int, exponent: int, modulus: int) -> int:
        """Быстрое возведение в степень по модулю с логированием"""
        result = 1
        base = base % modulus
        self._registry.add_log(f"Начальные значения: base={base}, exponent={exponent}, modulus={modulus}")

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
                self._registry.add_log(f"Нечетный показатель → result = {result}")
            base = (base * base) % modulus
            exponent = exponent // 2
            self._registry.add_log(f"exponent = {exponent}, base = {base}")

        return result

    def get_logs(self) -> Iterable[str]:
        """
        Возвращает логи
        """
        return self._registry.logs
