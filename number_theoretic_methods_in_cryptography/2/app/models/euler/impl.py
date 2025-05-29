from math import gcd
from typing import Final, Iterable, override

from app.core.registry import LogRegistry
from app.models.euler.interface import EulerModelInterface


class EulerModel(EulerModelInterface):
    def __init__(self) -> None:
        """
        Инициализирует модель для решения сравнения первой степени
        с использованием функции Эйлера.

        Внутренний логгер `LogRegistry` используется для отслеживания
        шагов вычислений.
        """
        self._registry: Final[LogRegistry] = LogRegistry()

    @override
    def solve_congruence(self, a: int, b: int, n: int) -> int | None:
        """
        Решает сравнение a * x ≡ b (mod n) с использованием теоремы Эйлера.

        Алгоритм:
        1. Проверяет, что a и n взаимно просты (НОД(a, n) == 1).
           Если нет — решение невозможно.
        2. Вычисляет φ(n) — количество чисел, взаимно простых с n.
        3. Находит обратный элемент a⁻¹ ≡ a^(φ(n)-1) mod n.
        4. Вычисляет x ≡ b * a⁻¹ mod n.

        Параметры:
            a (int): Коэффициент при x в сравнении.
            b (int): Константа в правой части сравнения.
            n (int): Модуль сравнения.

        Возвращает:
            int | None: Решение x, если существует. Иначе None.
        """

        # Проверка на существование решения
        if gcd(a, n) != 1:
            self._registry.add_log("Ошибка: a и n не взаимно просты. Решение не существует.")
            return None

        self._registry.add_log(f"Проверка: НОД({a}, {n}) = 1 -> решение существует")

        # Вычисление φ(n)
        phi: int = self._euler_phi(n)

        # Нахождение обратного элемента a^(-1) mod n
        inv_a: int = self._mod_inverse(a, n, phi)

        # Решение x ≡ b * a^(-1) mod n
        x: int = (b * inv_a) % n
        self._registry.add_log(f"Решение: x ≡ {b} * {inv_a} mod {n} -> x = {x}")

        return x

    def _euler_phi(self, n: int) -> int:
        """
        Вычисляет функцию Эйлера φ(n) — количество целых чисел от 1 до n-1,
        взаимно простых с n.

        Алгоритм:
        1. Начинает с φ(n) = n.
        2. Для каждого простого множителя i числа n:
           - Обновляет φ(n) по формуле: φ(n) = φ(n) * (1 - 1/i).
        3. Если после разложения остался множитель > 1, применяет формулу к нему.

        Параметры:
            n (int): Число, для которого вычисляется φ(n).

        Возвращает:
            int: Значение функции Эйлера φ(n).
        """
        result: int = n

        self._registry.add_log(f"φ({n}) = {n}")

        i: int = 2

        while i * i <= n:
            if n % i == 0:

                self._registry.add_log(f"Найден простой множитель: {i}")

                while n % i == 0:
                    n //= i

                result -= result // i

                self._registry.add_log(f"φ(n) = {result}")

            i += 1

        if n > 1:
            self._registry.add_log(f"Остаточный множитель: {n}")
            result -= result // n
            self._registry.add_log(f"φ(n) = {result}")

        return result

    def _mod_inverse(self, a: int, n: int, phi: int) -> int:
        """
        Находит обратный элемент a⁻¹ по модулю n через теорему Эйлера:
        a⁻¹ ≡ a^(φ(n)-1) mod n.

        Параметры:
            a (int): Число, для которого находится обратный элемент.
            n (int): Модуль.
            phi (int): Значение функции Эйлера φ(n).

        Возвращает:
            int: Обратный элемент a⁻¹ mod n.
        """
        exponent: int = phi - 1

        self._registry.add_log(f"Теорема Эйлера: a^(-1) ≡ a^{phi - 1} mod {n}")

        return self._modular_pow(a, exponent, n)

    def _modular_pow(self, base: int, exponent: int, modulus: int) -> int:
        """
        Быстрое возведение в степень по модулю.

        Алгоритм:
        1. Начинает с результата = 1.
        2. Пока показатель степени > 0:
           - Если показатель нечетный — умножает результат на base и берет mod.
           - Возводит base в квадрат и делит показатель на 2.
        3. Возвращает результат.

        Параметры:
            base (int): Основание степени.
            exponent (int): Показатель степени.
            modulus (int): Модуль.

        Возвращает:
            int: Результат base^exponent mod modulus.
        """
        result: int = 1
        base %= modulus
        self._registry.add_log(f"Начальные значения: base={base}, exponent={exponent}, modulus={modulus}")

        while exponent > 0:

            if exponent % 2 == 1:
                result: int = (result * base) % modulus
                self._registry.add_log(f"Нечетный показатель -> result = {result}")

            base = (base * base) % modulus
            exponent: int = exponent // 2

            self._registry.add_log(f"exponent = {exponent}, base = {base}")

        self._registry.add_log(f"Обратный элемент найден: {result}")
        return result

    def get_logs(self) -> Iterable[str]:
        """
        Быстрое возведение в степень по модулю.

        Алгоритм:
        1. Начинает с результата = 1.
        2. Пока показатель степени > 0:
           - Если показатель нечетный — умножает результат на base и берет mod.
           - Возводит base в квадрат и делит показатель на 2.
        3. Возвращает результат.

        Параметры:
            base (int): Основание степени.
            exponent (int): Показатель степени.
            modulus (int): Модуль.

        Возвращает:
            int: Результат base^exponent mod modulus.
        """
        return self._registry.logs
