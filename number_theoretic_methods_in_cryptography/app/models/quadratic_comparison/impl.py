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
        """
        Решает квадратичное сравнение x² ≡ number (mod prime) по алгоритму Тоннели-Шенкса.
        
        Алгоритм Тоннели-Шенкса — эффективный алгоритм для нахождения квадратных корней
        по модулю нечётного простого числа. Он работает за O(log² p) операций.
        
        Args:
            number: Число, для которого ищется квадратный корень
            prime: Нечётное простое число (модуль)
            
        Returns:
            tuple[int, int]: Два корня квадратного сравнения (x₁, x₂), где x₂ = p - x₁
            
        Raises:
            ModulusMustBeAnOddPrimeNumberError: Если prime не является нечётным простым числом
            NotAQuadraticDeductionError: Если number не является квадратичным вычетом по модулю prime
        """

        # Шаг 1: Проверка входных данных
        # Модуль должен быть нечётным простым числом (алгоритм не работает для p = 2)
        if not self.__is_prime(prime) or prime == 2:
            raise ModulusMustBeAnOddPrimeNumberError("Модуль должен быть нечётным простым числом")

        # Шаг 2: Проверка квадратичной вычетности
        # Если символ Лежандра (number/prime) ≠ 1, то number не является квадратичным вычетом
        # и квадратное сравнение не имеет решений
        legendre: int = self.__compute_legendre_symbol(number, prime)
        self._registry.add_log(f"Символ Лежандра ({number}/{prime}) = {legendre}")

        if legendre != 1:
            raise NotAQuadraticDeductionError(f"{number} не является квадратичным вычетом по модулю {prime}")

        # Шаг 3: Поиск квадратичного невычета
        # Квадратичный невычет z необходим для работы алгоритма Тоннели-Шенкса
        # Он используется для построения корректирующих множителей в процессе вычисления
        non_residue = self.__find_min_quadratic_non_residue(prime)
        self._registry.add_log(f"Минимальный квадратичный невычет: {non_residue}")

        # Шаг 4: Применение алгоритма Тоннели-Шенкса для нахождения корней
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
        """
        Вычисляет квадратные корни по алгоритму Тоннели-Шенкса.
        
        Алгоритм Тоннели-Шенкса решает квадратичное сравнение x² ≡ number (mod prime):
        
        1. Разложение: p-1 = q * 2^s, где q — нечётное число, s ≥ 1
        2. Инициализация:
           - m = s (текущая степень двойки)
           - c = z^q mod p (где z — квадратичный невычет)
           - t = a^q mod p (где a — число, для которого ищем корень)
           - r = a^((q+1)/2) mod p (начальное приближение корня)
        3. Основной цикл (пока t ≠ 1):
           - Находим минимальное i такое, что t^(2^i) ≡ 1 (mod p)
           - Вычисляем b = c^(2^(m-i-1)) mod p
           - Обновляем: r = r * b, t = t * b², c = b², m = i
        
        Args:
            number: Число, для которого ищется квадратный корень (должно быть квадратичным вычетом)
            prime: Нечётное простое число (модуль)
            quadratic_nonresidue: Квадратичный невычет по модулю prime
            
        Returns:
            tuple[int, int]: Два корня квадратного сравнения (x₁, x₂)
        """
        self._registry.add_log(f"Алгоритм Тонелли-Шенкса для x² = {number} mod {prime}")

        # Проверка: number должен быть квадратичным вычетом
        # Это необходимое условие для существования решения
        legendre = self.__compute_legendre_symbol(number, prime)
        if legendre != 1:
            raise ValueError(f"{number} не является квадратичным вычетом по модулю {prime}")

        # Шаг 1: Разложение p-1 = odd_factor * 2^exponent
        # Находим максимальную степень двойки, на которую делится p-1
        # Это нужно для определения структуры мультипликативной группы по модулю p
        odd_factor: int = prime - 1
        exponent: int = 0
        while odd_factor % 2 == 0:
            odd_factor //= 2
            exponent += 1

        self._registry.add_log(f"Разложение: {prime}-1 = {odd_factor} * 2^{exponent}")

        # Шаг 2: Инициализация параметров алгоритма
        # current_exponent: текущая степень двойки в разложении (начинаем с максимальной)
        # c_value: c = z^q mod p, где z — квадратичный невычет (используется для коррекции)
        # t_value: t = a^q mod p (проверяем, когда станет равным 1)
        # root_candidate: r = a^((q+1)/2) mod p (начальное приближение корня)
        current_exponent: int = exponent
        c_value: int = pow(quadratic_nonresidue, odd_factor, prime)
        t_value: int = pow(number, odd_factor, prime)
        root_candidate: int = pow(number, (odd_factor + 1) // 2, prime)

        self._registry.add_log(
            f"Инициализация: exponent={current_exponent}, "
            f"c={c_value}, t={t_value}, root={root_candidate}"
        )

        # Шаг 3: Главный цикл алгоритма
        # Продолжаем, пока t ≠ 1. Когда t = 1, мы нашли корень
        while t_value != 1:
            # Поиск минимального i такого, что t^(2^i) ≡ 1 (mod p)
            # Это определяет, насколько нужно "сдвинуть" текущую степень двойки
            min_exp = 0
            temp_t = t_value
            while temp_t != 1:
                temp_t = pow(temp_t, 2, prime)
                min_exp += 1

            self._registry.add_log(f"Найдено i={min_exp} (t^(2^{min_exp}) = 1)")

            # Вычисление корректирующего множителя b
            # shift = m - i - 1 определяет степень, в которую нужно возвести c
            # b = c^(2^shift) mod p используется для коррекции текущего приближения
            shift: int = current_exponent - min_exp - 1
            b_value: int = pow(c_value, 1 << shift, prime)

            # Обновление параметров для следующей итерации
            # current_exponent = i: уменьшаем степень двойки
            # c_value = b²: обновляем корректирующий множитель
            # t_value = t * b²: приближаем t к 1
            # root_candidate = r * b: уточняем значение корня
            current_exponent: int = min_exp
            c_value: int = pow(b_value, 2, prime)
            t_value: int = (t_value * c_value) % prime
            root_candidate: int = (root_candidate * b_value) % prime

            self._registry.add_log(
                f"Обновление: exponent={current_exponent}, "
                f"c={c_value}, t={t_value}, root={root_candidate}"
            )

        # Шаг 4: Формирование результата
        # Если x — корень, то p - x также является корнем (так как x² ≡ (p-x)² mod p)
        root1: int = root_candidate
        root2: int = prime - root1
        self._registry.add_log(f"Найденные корни: {root1} и {root2}")
        return root1, root2



    def __find_min_quadratic_non_residue(self, prime: int) -> int:
        """
        Находит минимальный квадратичный невычет по модулю prime.
        
        Квадратичный невычет — это число z, для которого символ Лежандра (z/p) = -1,
        то есть z не является квадратом по модулю p. Такой элемент всегда существует
        для нечётного простого числа p и необходим для работы алгоритма Тоннели-Шенкса.
        
        Алгоритм: перебираем числа от 2 до p-1 и находим первое, для которого
        символ Лежандра равен -1 (что в модульной арифметике соответствует p-1).
        
        Args:
            prime: Нечётное простое число
            
        Returns:
            int: Минимальный квадратичный невычет по модулю prime
            
        Raises:
            ValueError: Если квадратичный невычет не найден (не должно происходить для простых p > 2)
        """
        # Перебираем кандидатов от 2 до p-1
        # Для простого числа p > 2 всегда существует квадратичный невычет
        for candidate in range(2, prime):
            # Символ Лежандра равен -1, что в модульной арифметике соответствует p-1
            if self.__compute_legendre_symbol(candidate, prime) == prime - 1:  # -1 mod prime
                return candidate
        raise ValueError(f"Не найден квадратичный невычет для {prime}")

    def __compute_legendre_symbol(self, base: int, prime: int) -> int:
        """
        Вычисляет символ Лежандра (base/prime) по формуле Эйлера.
        
        Символ Лежандра (a/p) для простого числа p определяется как:
        - 0, если a ≡ 0 (mod p)
        - 1, если a — квадратичный вычет по модулю p (существует x: x² ≡ a mod p)
        - -1, если a — квадратичный невычет по модулю p
        
        Формула Эйлера: (a/p) ≡ a^((p-1)/2) (mod p)
        Результат всегда равен 0, 1 или p-1 (где p-1 интерпретируется как -1).
        
        Args:
            base: Число, для которого вычисляется символ Лежандра
            prime: Нечётное простое число (модуль)
            
        Returns:
            int: Символ Лежандра (0, 1 или prime-1, где prime-1 означает -1)
        """
        # Формула Эйлера: символ Лежандра равен a^((p-1)/2) mod p
        exponent: int = (prime - 1) // 2
        result: int = pow(base, exponent, prime)

        self._registry.add_log(
            f"Символ Лежандра ({base}/{prime}) = {result if result != prime - 1 else f'{result} (= -1)'}")
        return result

    @staticmethod
    def __is_prime(number: int) -> bool:
        """
        Проверяет, является ли число простым методом пробного деления.
        
        Алгоритм:
        1. Числа меньше 2 не являются простыми
        2. 2 — единственное чётное простое число
        3. Для нечётных чисел проверяем делимость на нечётные числа от 3 до √n
        
        Args:
            number: Число для проверки
            
        Returns:
            bool: True, если number является простым числом, иначе False
        """
        # Числа меньше 2 не являются простыми
        if number < 2:
            return False
        # 2 — единственное чётное простое число
        if number == 2:
            return True
        # Все остальные чётные числа составные
        if number % 2 == 0:
            return False

        # Проверяем делимость на нечётные числа от 3 до √n
        # Достаточно проверить до квадратного корня, так как если есть делитель > √n,
        # то есть и делитель < √n
        limit = math.isqrt(number)
        for divisor in range(3, limit + 1, 2):
            if number % divisor == 0:
                return False
        return True
