from typing import List, Tuple, Optional, Final

from app.core.registry import LogRegistry


class ContinuedFractionModel:
    def __init__(self):
        self._registry: Final[LogRegistry] = LogRegistry()

    def solve_linear_congruence(self, a: int, b: int, m: int) -> Optional[int]:
        """
        Решает сравнение ax ≡ b (mod m) с помощью непрерывных дробей
        в соответствии с подходом, показанным на фото
        """
        self._registry.add_log(f"Решаем сравнение: {a}x ≡ {b} (mod {m})")
        self._registry.add_log(f"Преобразуем: x ≡ {b}/{a} (mod {m})")

        # Шаг 1: Построение цепной дроби для m/a
        continued_fraction = self.get_continued_fraction(m, a)
        self._registry.add_log(f"Цепная дробь: {continued_fraction}")

        # Шаг 2: Восстановление дроби
        numerator, denominator = self.compute_fraction_from_continued_fraction(continued_fraction)
        self._registry.add_log(f"Восстановленная дробь: {numerator}/{denominator}")

        # Шаг 3: Вычисление таблицы P и Q
        p_table, q_table = self.compute_pq_tables_csharp_style(continued_fraction)

        # Шаг 4: Нахождение Pk (предпоследнее значение)
        pk = p_table[len(continued_fraction) - 1]
        self._registry.add_log(f"Pk = {pk}")

        # Шаг 5: Вычисление решения
        solution = (pk * b) % m
        self._registry.add_log(f"Ответ: x ≡ {solution} (mod {m})")

        # Нормализация решения
        solution %= m
        if solution < 0:
            solution += m
        self._registry.add_log(f"x = {solution}")

        return solution

    def get_continued_fraction(self, numerator: int, denominator: int) -> List[int]:
        """Вычисляет цепную дробь для числа numerator/denominator"""
        coefficients = []
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

        # Начинаем с последнего элемента
        num = 1
        denom = coefficients[-1]

        # Обратный обход коэффициентов
        for coeff in reversed(coefficients[:-1]):
            num, denom = denom, coeff * denom + num

        return denom, num

    def compute_pq_tables_csharp_style(self, coefficients: List[int]) -> Tuple[List[int], List[int]]:
        """Вычисляет таблицы Pk и Qk в стиле C# кода"""
        n = len(coefficients)
        p_table = [0] * (n + 1)
        q_table = [0] * (n + 1)

        # Инициализация таблиц
        p_table[0] = 1
        q_table[0] = 0

        if n > 0:
            p_table[1] = coefficients[0]
            q_table[1] = 1

        # Заполняем таблицы
        for i in range(2, n + 1):
            p_table[i] = coefficients[i - 1] * p_table[i - 1] + p_table[i - 2]
            q_table[i] = coefficients[i - 1] * q_table[i - 1] + q_table[i - 2]

        # Логирование таблицы в стиле фото
        self._registry.add_log("\nТаблица вычислений:")
        self._registry.add_log(f"{'k':<3} | {'a_k':<8} | {'P':<8} | {'Q':<8}")
        self._registry.add_log("-" * 30)

        # Специальная строка для k=0
        self._registry.add_log(f"{0:<3} | {'':<8} | {0:<8} | {1:<8}")

        # Вывод строк таблицы
        for i in range(1, n + 1):
            a_k = coefficients[i - 1] if i - 1 < len(coefficients) else ""
            self._registry.add_log(f"{i:<3} | {a_k:<8} | {q_table[i]:<8} | {p_table[i]:<8}")

        return p_table, q_table

    @property
    def logs(self) -> List[str]:
        return self._registry.logs

if __name__ == "__main__":
    model = ContinuedFractionModel()
    solution = model.solve_linear_congruence(183, 93, 111)
    print(f"Решение: x ≡ {solution} (mod 111)")

    print("\nЛоги вычислений:")
    for log in model.logs:
        print(log)