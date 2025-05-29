"""
Вычислить НОД(a, b) при помощи алгоритма Евклида с делением с остатком;
"""
from typing import override

from app.models.euclidian_algorithms.base import NumberType, ResultDTO, BaseGCDStrategy


class GCDMod(BaseGCDStrategy):
    @override
    def compute(self, a: NumberType, b: NumberType) -> ResultDTO:
        """
        Вычисляет НОД(a, b) с использованием классического алгоритма Евклида,
        основанного на делении с остатком.

        Алгоритм:
        1. Приводим оба числа к положительному виду (по модулю)
        2. Пока второе число (b) не равно нулю:
           - Заменяем a на b
           - Заменяем b на остаток от деления предыдущего a на b
        3. Как только b становится равным нулю, текущее значение a
           является наибольшим общим делителем.

        Особенности:
        - Работает эффективно благодаря использованию операции остатка (%)
        - Обрабатывает все целые числа, включая отрицательные
        - Возвращает 0 при НОД(0, 0) согласно соглашению

        Args:
            a: Первое целое число
            b: Второе целое число

        Returns:
            NumberType: Наибольший общий делитель чисел a и b
        """
        a: NumberType = abs(a)
        b: NumberType = abs(b)

        self._registry.add_log(f"Исходное значение - {a=}, {b=}")

        while b != 0:
            a, b = b, a % b
            self._registry.add_log(f"Новые после a % b: {a=}, {b=}")
            self._iterations += 1

        return ResultDTO(greatest_common_divisor=a)
