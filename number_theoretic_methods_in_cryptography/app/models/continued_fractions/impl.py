from typing import List, Final, Iterable, override

from app.core.registry import LogRegistry
from app.models.continued_fractions.base import IContinuedFractionModel


class ContinuedFractionModel(IContinuedFractionModel):
    def __init__(self):
        self._registry: Final[LogRegistry] = LogRegistry()

    @override
    def solve_linear_congruence(self, a: int, b: int, m: int) -> int:
        """
        Решает сравнение ax ≡ b (mod m) с помощью непрерывных дробей.
        
        Алгоритм основан на методе решения сравнения первой степени через:
        1. Преобразование в уравнение ax + my = b
        2. Вычисление НОД(a, m) бинарным алгоритмом
        3. Разложение дроби m/a в непрерывную дробь
        4. Вычисление подходящих дробей
        5. Нахождение частного решения по формуле
        """
        self._registry.add_log(f"Решаем сравнение: {a}x ≡ {b} (mod {m})")
        
        # Шаг 1: Преобразование сравнения
        self._registry.add_log(f"Шаг 1: Преобразование сравнения")
        self._registry.add_log(f"{a}x = {b} (mod {m}) равносильно {a}x + {m}y = {b}")
        
        a_coefficient: int = a
        b_coefficient: int = m
        c_value: int = b
        
        # Шаг 2: Вычисление НОД(a, m)
        self._registry.add_log(f"Шаг 2: Вычисление НОД(a, m)")
        d_value = self.__binary_gcd(a_coefficient, b_coefficient)
        self._registry.add_log(f"НОД({a_coefficient}, {b_coefficient}) = {d_value}")
        
        # Проверка существования решения
        if c_value % d_value != 0:
            self._registry.add_log(f"Ошибка: {c_value} не делится на {d_value}")
            self._registry.add_log(f"Уравнение {a_coefficient}x + {b_coefficient}y = {c_value} не имеет решений")
            raise ValueError(f"Сравнение {a}x = {b} (mod {m}) не имеет решений")
        
        self._registry.add_log(f"{c_value} делится на {d_value}, уравнение имеет решения")
        
        # Шаг 3: Разложение дроби в непрерывную дробь
        self._registry.add_log(f"Шаг 3: Разложение дроби в непрерывную дробь")
        coefficients = self.__get_continued_fraction_for_rational(a_coefficient, b_coefficient)
        
        # Шаг 4: Вычисление подходящих дробей
        self._registry.add_log(f"Шаг 4: Вычисление подходящих дробей")
        
        if len(coefficients) == 1:
            drob_str = f"[{coefficients[0]}]"
        else:
            main_part = str(coefficients[0])
            rest_parts = []
            for i in range(1, len(coefficients)):
                rest_parts.append(f"1/{coefficients[i]}")
            drob_str = f"[{main_part}; {', '.join(rest_parts)}]"
        
        self._registry.add_log(f"Непрерывная дробь: {drob_str}")
        
        table_data = self.__compute_convergent_fractions(coefficients)
        
        # Шаг 5: Нахождение общего решения
        self._registry.add_log(f"Шаг 5: Нахождение общего решения")
        
        # Находим максимальный k
        k = 0
        for row in table_data[1:]:
            try:
                row_k = int(row[0])
                if row_k > k:
                    k = row_k
            except (ValueError, IndexError):
                continue
        
        # Берем предпоследнюю строку (P_{k-1} и Q_{k-1})
        if len(table_data) >= 3:
            prev_row = table_data[-2]
            if len(prev_row) >= 5:
                try:
                    P_k_minus_1 = int(prev_row[3])
                    Q_k_minus_1 = int(prev_row[4])
                except (ValueError, IndexError):
                    raise ValueError("Ошибка при чтении значений из таблицы")
            else:
                raise ValueError("Недостаточно данных в таблице")
        else:
            raise ValueError("Таблица вычислений некорректна")
        
        self._registry.add_log(f"k = {k}, P_{k - 1} = {P_k_minus_1}, Q_{k - 1} = {Q_k_minus_1}")
        
        sign = (-1) ** (k - 1)
        multiplier = c_value // d_value
        
        self._registry.add_log(f"Формулы общего решения:")
        self._registry.add_log(f"x = (-1)^{k - 1} × (c/d) × Q_{k - 1} + m × t")
        self._registry.add_log(f"y = (-1)^{k - 1} × (c/d) × P_{k - 1} + a × t")
        self._registry.add_log(f"x = {sign} × {multiplier} × {Q_k_minus_1} + {b_coefficient} × t")
        self._registry.add_log(f"y = {sign} × {multiplier} × {P_k_minus_1} + {a_coefficient} × t")
        
        # Вычисляем частное решение (для t = 0)
        x_solution = sign * multiplier * Q_k_minus_1
        
        # Нормализация решения по модулю m
        x_solution = x_solution % m
        if x_solution < 0:
            x_solution += m
        
        self._registry.add_log(f"Частное решение (t = 0): x = {x_solution} (mod {m})")
        
        return x_solution

    def __binary_gcd(self, a: int, b: int) -> int:
        """
        Вычисляет НОД(a, b) бинарным алгоритмом Евклида.
        
        Алгоритм:
        1. Если одно из чисел равно 0, возвращаем другое
        2. Если числа равны, возвращаем это число
        3. Убираем общие множители 2, запоминая степень
        4. Пока числа не равны:
           - Если оба четные: делим на 2, увеличиваем степень
           - Если одно четное: делим его на 2
           - Если оба нечетные: вычитаем меньшее из большего
        5. Возвращаем результат, умноженный на 2^степень
        """
        if a == 0:
            return abs(b)
        if b == 0:
            return abs(a)
        if a == b:
            return abs(a)
        
        a = abs(a)
        b = abs(b)
        
        stepen = 0
        
        while a != b:
            if (a % 2 == 0) and (b % 2 == 0):
                a //= 2
                b //= 2
                stepen += 1
                continue
            if (a % 2 == 0) and (b % 2 == 1):
                a //= 2
                continue
            if (a % 2 == 1) and (b % 2 == 0):
                b //= 2
                continue
            if (a % 2 == 1) and (b % 2 == 1):
                if a > b:
                    a = a - b
                else:
                    b = b - a
                continue
        
        return a * (2 ** stepen)

    def __get_continued_fraction_for_rational(self, chislitel: int, znamenatel: int) -> List[int]:
        """
        Разлагает рациональную дробь chislitel/znamenatel в непрерывную дробь.
        
        Логика соответствует zadanie_1_ra из lab_7_tchmk.py:
        - Если дробь отрицательная, выделяем целую часть
        - Если правильная дробь (|chislitel| < |znamenatel|), добавляем 0
        - Применяем алгоритм Евклида для получения коэффициентов
        
        Возвращает список коэффициентов [a0, a1, a2, ...]
        """
        coefficients: list[int] = []
        
        # Обрабатываем случай отрицательных чисел
        if chislitel < 0:
            celaya_chast = chislitel // znamenatel
            ostatok = chislitel % znamenatel
            a = abs(znamenatel)
            b = abs(ostatok)
            if celaya_chast != 0:
                coefficients.append(celaya_chast)
        else:
            if abs(chislitel) < abs(znamenatel):
                # Правильная дробь - добавляем 0 в начало
                a = abs(znamenatel)
                b = abs(chislitel)
                coefficients.append(0)
            else:
                # Неправильная дробь
                a = max(abs(chislitel), abs(znamenatel))
                b = min(abs(chislitel), abs(znamenatel))
        
        # Алгоритм Евклида для получения коэффициентов
        step = 1
        while b != 0:
            quotient = a // b
            remainder = a % b
            coefficients.append(quotient)
            
            self._registry.add_log(f"Шаг {step}: {a} = {b} × {quotient} + {remainder}")
            
            a, b = b, remainder
            step += 1
        
        return coefficients

    def __compute_convergent_fractions(self, coefficients: List[int]) -> List[List[str]]:
        """
        Вычисляет подходящие дроби для непрерывной дроби.
        
        Возвращает таблицу вида:
        [["k", "b_k", "a_k", "P_k", "Q_k"], ...]
        
        Формулы:
        P_{-1} = 1, Q_{-1} = 0
        P_0 = a_0, Q_0 = 1
        P_k = a_k * P_{k-1} + b_k * P_{k-2}
        Q_k = a_k * Q_{k-1} + b_k * Q_{k-2}
        
        Для обычной непрерывной дроби b_k = 1 для всех k.
        """
        table_data: list[list[str]] = [["k", "b_k", "a_k", "P_k", "Q_k"], ["-1", "", "", "1", "0"]]

        if not coefficients:
            return table_data
        
        # Инициализация
        P_prev2 = 1
        Q_prev2 = 0
        
        P_prev1 = coefficients[0]
        Q_prev1 = 1
        
        table_data.append(["0", "1", str(coefficients[0]), str(P_prev1), str(Q_prev1)])
        
        self._registry.add_log(f"Инициализация:")
        self._registry.add_log(f"P₋₁ = 1, Q₋₁ = 0")
        self._registry.add_log(f"P₀ = a₀ = {coefficients[0]}, Q₀ = 1")
        
        if len(coefficients) == 1:
            return table_data
        
        # Вычисление подходящих дробей
        for k in range(1, len(coefficients)):
            b_k = 1  # Для обычной непрерывной дроби b_k всегда 1
            a_k = coefficients[k]
            
            P_k = a_k * P_prev1 + b_k * P_prev2
            Q_k = a_k * Q_prev1 + b_k * Q_prev2
            
            table_data.append([str(k), str(b_k), str(a_k), str(P_k), str(Q_k)])
            
            self._registry.add_log(f"Шаг {k} (b_{k} = {b_k}, a_{k} = {a_k}):")
            self._registry.add_log(f"P_{k} = a_{k} × P_{k - 1} + b_{k} × P_{k - 2} = {a_k} × {P_prev1} + {b_k} × {P_prev2} = {P_k}")
            self._registry.add_log(f"Q_{k} = a_{k} × Q_{k - 1} + b_{k} × Q_{k - 2} = {a_k} × {Q_prev1} + {b_k} × {Q_prev2} = {Q_k}")
            self._registry.add_log(f"Подходящая дробь {k}: P_{k}/Q_{k} = {P_k}/{Q_k}")
            
            P_prev2, Q_prev2 = P_prev1, Q_prev1
            P_prev1, Q_prev1 = P_k, Q_k
        
        # Логирование таблицы
        self._registry.add_log("\nТаблица вычислений:")
        self._registry.add_log(f"{'k':<3} | {'b_k':<5} | {'a_k':<8} | {'P_k':<8} | {'Q_k':<8}")
        self._registry.add_log("-" * 40)
        for row in table_data:
            if len(row) >= 5:
                self._registry.add_log(f"{row[0]:<3} | {row[1]:<5} | {row[2]:<8} | {row[3]:<8} | {row[4]:<8}")
        
        return table_data

    @override
    def get_logs(self) -> Iterable[str]:
        return self._registry.logs
