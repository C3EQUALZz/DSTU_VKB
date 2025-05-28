"""
Вычислить НОД(a, b) при помощи бинарного алгоритма Евклида.
"""
from typing import override

from app.core.dto import NumberType, ResultDTO
from app.models.base import BaseGCDStrategy


class GCDBinary(BaseGCDStrategy):
    @override
    def compute(self, a: NumberType, b: NumberType) -> ResultDTO:
        """
        Вычисляет НОД(a, b) с использованием бинарного алгоритма Евклида (алгоритм Штейна).

        Алгоритм Штейна:
        1. Если одно из чисел равно 0, возвращаем другое.
        2. Убираем общие множители 2 из a и b, запоминая степень (k).
        3. Убираем оставшиеся множители 2 из a, если a чётное.
        4. Пока b ≠ 0:
           - Убираем множители 2 из b
           - Если a > b, меняем их местами
           - Выполняем b = b - a (a всегда нечётное)
        5. Возвращаем a * 2^k — восстанавливаем общие множители 2

        Преимущества:
        - Использует побитовые операции вместо деления, что быстрее на больших числах
        - Эффективен в системах с ограниченными вычислительными ресурсами

        Особенности:
        - Обрабатывает отрицательные числа через абсолютное значение
        - Возвращает 0 при НОД(0, 0) (математически не определён)

        Args:
            a: Первое целое число
            b: Второе целое число

        Returns:
            NumberType: Наибольший общий делитель чисел a и b
        """

        # Шаг 1: Обработка нулей
        if a == 0:
            self._registry.add_log(f"a=0, поэтому результат {b=}")
            return ResultDTO(greatest_common_divisor=b)
        if b == 0:
            self._registry.add_log(f"b=0, поэтому результат {a=}")
            return ResultDTO(greatest_common_divisor=a)

        # Приводим числа к положительному виду
        a: NumberType = abs(a)
        b: NumberType = abs(b)

        self._registry.add_log(f"Поставили обоих в модуль: a={a}, b={b}")

        # Шаг 2: Находим максимальную степень 2, делящую оба числа
        k: int = 0
        self._registry.add_log(f"Находим максимальную степень 2, делящую оба числа: {k=}")

        while ((a | b) & 1) == 0:  # Проверка, чётны ли оба числа
            a >>= 1  # Делим a на 2
            b >>= 1  # Делим b на 2
            k += 1  # Увеличиваем степень
            self._registry.add_log(f"Пока два числа не четны, поэтому работаем: a/2 = {a}, b/2 = {b}, {k=}")
            self._iterations += 1

        self._registry.add_log(f"Начинаем проверку, что есть ли множители 2 в а, {a=}")
        # Шаг 3: Убираем оставшиеся множители 2 из a
        while (a & 1) == 0:  # Проверка, чётное ли a
            a >>= 1  # Делим a на 2
            self._registry.add_log(f"Результат {a=}")
            self._iterations += 1

        self._registry.add_log(f"Теперь a - нечетное, {a=}")
        # Теперь a — нечётное число
        while b != 0:
            self._iterations += 1  # Считаем внешний цикл

            # Шаг 4.1: Убираем множители 2 из b
            while (b & 1) == 0:  # Проверка, чётное ли b
                b >>= 1  # Делим b на 2
                self._registry.add_log(f"b/2 = {b}")
                self._iterations += 1  # Считаем внутренний цикл

            # Шаг 4.2: Меняем местами, если a > b
            if a > b:
                self._registry.add_log("a > b, меняем местами: {a=}, {b=}")
                a, b = b, a

            # Шаг 4.3: Выполняем вычитание
            b -= a
            self._registry.add_log(f"Выполняем вычитания - {b=}")

        # Шаг 5: Восстанавливаем общие множители 2
        # Умножаем результат на 2^k
        result: NumberType = a << k
        self._registry.add_log(f"Умножаем результат на 2 ^ k - {result}")

        return ResultDTO(greatest_common_divisor=result)
