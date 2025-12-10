import math
from typing import List, Tuple, Final, Iterable

from app.core.registry import LogRegistry
from app.exceptions.models.congruence import NoSolutionSinceGCDDoesNotShareFreeTermError


class ContinuedFractionModel:
    """
    Модель для решения сравнения первой степени ax ≡ b (mod m)
    с использованием непрерывных дробей и подходящих дробей.
    Алгоритм повторяет логику из лабораторной работы:
      1. Проверяем существование решения по НОД.
      2. Упрощаем сравнение, деля на НОД.
      3. Строим цепную дробь для a/m.
      4. Считаем подходящие дроби (P_k, Q_k).
      5. По формуле получаем решение x.
    """

    def __init__(self):
        self._registry: Final[LogRegistry] = LogRegistry()

    def solve_linear_congruence(self, a: int, b: int, m: int) -> int:
        """
        Решает сравнение ax ≡ b (mod m) через непрерывные дроби.
        Возвращает одно корректное решение x по модулю m.
        """
        self._registry.clear_logs()
        self._registry.add_log(f"Решаем сравнение: {a}x = {b} (mod {m})")

        # 1. Проверка существования решения
        gcd_value = math.gcd(a, m)
        self._registry.add_log(f"НОД({a}, {m}) = {gcd_value}")
        if b % gcd_value != 0:
            raise NoSolutionSinceGCDDoesNotShareFreeTermError(
                "Решение не существует, так как НОД не делит свободный член."
            )

        # 2. Упрощаем сравнение
        a_simplified = a // gcd_value
        b_simplified = b // gcd_value
        m_simplified = m // gcd_value
        self._registry.add_log(
            f"Упрощенное сравнение: {a_simplified}x = {b_simplified} (mod {m_simplified})"
        )

        # 3. Построение цепной дроби для a_simplified / m_simplified
        self._registry.add_log("Разлагаем дробь a/m в непрерывную:")
        coefficients = self.get_continued_fraction(a_simplified, m_simplified)
        self._registry.add_log(f"Коэффициенты цепной дроби: {coefficients}")

        x_solution: int

        if len(coefficients) < 2:
            # Для формулы решения нужен хотя бы один подходящий элемент
            self._registry.add_log(
                "Цепная дробь имеет длину 1, используем обратный элемент по модулю."
            )
            x_solution = (b_simplified * pow(a_simplified, -1, m_simplified)) % m_simplified
        else:
            # 4. Считаем подходящие дроби (convergents)
            p_table, q_table = self.compute_pq_tables(coefficients)

            # k = последняя строка таблицы (индексация с нуля)
            k = len(coefficients) - 1
            q_prev = q_table[k - 1]  # Q_{k-1}
            self._registry.add_log(f"k = {k}, Q_(k-1) = {q_prev}")

            # 5. Формула решения: x = (-1)^(k-1) * (b/d) * Q_{k-1} (mod m/d)
            sign = -1 if (k - 1) % 2 else 1
            x_raw = sign * b_simplified * q_prev
            x_solution = x_raw % m_simplified
            self._registry.add_log(
                f"x = (-1)^({k-1}) * {b_simplified} * {q_prev} (mod {m_simplified}) = {x_solution}"
            )

        # Возвращаем решение к исходному модулю
        x_solution %= m_simplified
        if x_solution < 0:
            x_solution += m_simplified
        self._registry.add_log(f"Частное решение: x = {x_solution} (mod {m_simplified})")

        # Если gcd > 1, формируем все решения как в теореме: x0 + k * m1, k=0..d-1
        if gcd_value > 1:
            m1 = m_simplified
            all_solutions = sorted({(x_solution + k * m1) % m for k in range(gcd_value)})
            self._registry.add_log(
                f"НОД = {gcd_value} -> всего решений: {gcd_value}. m1 = m/d = {m1}"
            )
            for idx, sol in enumerate(all_solutions):
                self._registry.add_log(f"x_{idx} = {sol} (mod {m})")
        else:
            self._registry.add_log("НОД = 1 -> единственное решение.")
            self._registry.add_log(f"x = {x_solution} (mod {m})")

        # Проверка
        numerator = a * x_solution - b
        self._registry.add_log(f"Проверка: (a·x - b) / m = {numerator} / {m}")
        if numerator % m == 0:
            self._registry.add_log("✓ Проверка пройдена: делится нацело")
        else:
            self._registry.add_log(
                f"✗ Проверка не пройдена: остаток {numerator % m}"
            )

        return x_solution

    def get_continued_fraction(self, numerator: int, denominator: int) -> List[int]:
        """
        Вычисляет цепную дробь для числа numerator/denominator.
        Возвращает список коэффициентов [a0, a1, ...].
        """
        coefficients: List[int] = []
        self._registry.add_log(f"{'Числитель':<12} | {'Знаменатель':<12} | {'Частное'}")
        while denominator != 0:
            quotient = numerator // denominator
            remainder = numerator % denominator
            self._registry.add_log(f"{numerator:<12} | {denominator:<12} | {quotient}")
            coefficients.append(quotient)
            numerator, denominator = denominator, remainder
        return coefficients

    def compute_fraction_from_continued_fraction(self, coefficients: List[int]) -> Tuple[int, int]:
        """Восстанавливает дробь из цепной дроби"""
        if not coefficients:
            return 0, 1

        num = 1
        denom = coefficients[-1]
        for coeff in reversed(coefficients[:-1]):
            num, denom = denom, coeff * denom + num

        return denom, num

    def compute_pq_tables(self, coefficients: List[int]) -> Tuple[List[int], List[int]]:
        """
        Считает подходящие дроби.
        Возвращает списки P_i и Q_i длины len(coefficients).
        """
        n = len(coefficients)
        p_table: List[int] = [0] * n
        q_table: List[int] = [0] * n

        # Базовые значения
        p_prev2, q_prev2 = 1, 0                     # P_-1, Q_-1
        p_prev1, q_prev1 = coefficients[0], 1       # P_0, Q_0

        p_table[0] = p_prev1
        q_table[0] = q_prev1

        self._registry.add_log("\nТаблица подходящих дробей:")
        self._registry.add_log(f"{'k':<3} | {'a_k':<8} | {'P_k':<8} | {'Q_k':<8}")
        self._registry.add_log(f"{-1:<3} | {'':<8} | {p_prev2:<8} | {q_prev2:<8}")
        self._registry.add_log(f"{0:<3} | {coefficients[0]:<8} | {p_table[0]:<8} | {q_table[0]:<8}")

        # Рекуррентные расчёты
        for k in range(1, n):
            a_k = coefficients[k]
            p_k = a_k * p_prev1 + p_prev2
            q_k = a_k * q_prev1 + q_prev2

            p_table[k] = p_k
            q_table[k] = q_k

            self._registry.add_log(f"{k:<3} | {a_k:<8} | {p_k:<8} | {q_k:<8}")

            p_prev2, q_prev2 = p_prev1, q_prev1
            p_prev1, q_prev1 = p_k, q_k

        return p_table, q_table

    def get_logs(self) -> Iterable[str]:
        return self._registry.logs