import math
from dataclasses import dataclass
from typing_extensions import override

from cryptography_methods.domain.ceaser.errors import NumbersAreNotRelativelyPrime
from cryptography_methods.domain.common.values import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class KeyAffine(BaseValueObject):
    """
    Ключ шифрования для алгоритма: Аффинная система подстановок Цезаря.
    Здесь a, b - числовые ключи, которые задает пользователь.
    m - количество букв в алфавите.

    Должно выполняться такое правило, что НОД(a, m) = 1.
    """
    a: int
    b: int
    m: int

    @override
    def _validate(self) -> None:
        if any(field is None or not isinstance(field, int) for field in (self.a, self.b, self.m)):
            raise TypeError("values must be a integer")

        if math.gcd(self.a, self.m) != 1:
            raise NumbersAreNotRelativelyPrime(f"{self.a=} and {self.m=} must be relatively prime")

    @override
    def __str__(self) -> str:
        return f"{self.a=}, {self.b=}, {self.m=}"
