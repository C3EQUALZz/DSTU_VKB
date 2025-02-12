from typing import Callable
from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.exceptions.domain import BadOperationException


@dataclass(eq=False)
class FieldCalculator(BaseEntity):
    def __post_init__(self) -> None:
        super().__post_init__()

        self.operations: dict[str, Callable[[int, int, int], int]] = {
            "+": lambda a, b, mod: (a + b) % mod,
            "-": lambda a, b, mod: (a - b) % mod,
            "*": lambda a, b, mod: (a * b) % mod,
            "/": lambda a, b, mod: (a * self.__mod_inverse(b, mod)) % mod,
            "^": lambda a, b, mod: pow(a, b, mod),
        }

    def apply_operation(
            self,
            a: int,
            b: int,
            op: str,
            mod: int
    ) -> int:
        """Применяет арифметическую операцию в поле Z/modZ"""
        if op not in self.operations:
            raise BadOperationException(op)
        return self.operations[op](a, b, mod)

    def __mod_inverse(self, a: int, mod: int) -> int:
        """Возвращает обратное число a^(-1) в поле Z/modZ"""
        g, x, _ = self.__extended_gcd(a, mod)
        if g != 1:
            raise ValueError(f"Число {a} не имеет обратного по модулю {mod}")
        return x % mod

    @staticmethod
    def __extended_gcd(a: int, b: int):
        """
        Расширенный алгоритм Евклида для нахождения обратного элемента.

        old_r, r: Эти переменные хранят текущие и предыдущие значения остатков.
         old_r инициализируется значением a, а r — значением b.
        old_s, s: Эти переменные хранят коэффициенты для a.
         old_s инициализируется 1 (поскольку 1 * a = a), а s — 0 (поскольку 0 * b = 0).
        old_t, t: Эти переменные хранят коэффициенты для b.
        old_t инициализируется 0, а t — 1.
        """
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        while r:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_r, old_s, old_t
