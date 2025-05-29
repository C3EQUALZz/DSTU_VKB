from typing import override

from app.models.euclidian_algorithms.base import NumberType, ResultDTO, BaseGCDStrategy


class GCDBezout(BaseGCDStrategy):
    @override
    def compute(self, a: NumberType, b: NumberType) -> ResultDTO:
        """
        Вычисляет НОД(a, b) и коэффициенты Безу x и y, удовлетворяющие уравнению Безу:
            a * x + b * y = НОД(a, b)

        Алгоритм:
        1. Приводим числа a и b к положительным значениям (берём их абсолютные значения)
        2. Инициализируем начальные коэффициенты Безу:
           - current_coefficient_a = 1 (коэффициент при a)
           - next_coefficient_a = 0 (вспомогательный коэффициент)
           - current_coefficient_b = 0 (коэффициент при b)
           - next_coefficient_b = 1 (вспомогательный коэффициент)
        3. Пока b не равно нулю:
           - Вычисляем частное q = a // b
           - Обновляем остаток: a, b = b, a % b
           - Обновляем коэффициенты Безу по формулам:
             next_coefficient_a = current_coefficient_a - q * next_coefficient_a
             next_coefficient_b = current_coefficient_b - q * next_coefficient_b
           - Сдвигаем коэффициенты: current_coefficient_a, next_coefficient_a = next_coefficient_a, current_coefficient_a - quotient * next_coefficient_a
             (и аналогично для b)
        4. Возвращаем НОД(a, b), а также коэффициенты x и y

        Особенности:
        - Работает с любыми целыми числами, включая отрицательные
        - Возвращает положительный НОД
        - Коэффициенты x и y могут быть отрицательными

        Args:
            a: Первое целое число
            b: Второе целое число

        Returns:
            ResultDTO: Объект, содержащий НОД(a, b), x и y
        """

        # Шаг 1: Приводим числа к положительному виду
        a_abs: NumberType = abs(a)
        b_abs: NumberType = abs(b)

        self._registry.add_log(f"Привели числа к положительному виду: {a_abs=}, {b_abs=}")

        # Шаг 2: Инициализируем коэффициенты Безу
        current_coefficient_a, next_coefficient_a = 1, 0
        current_coefficient_b, next_coefficient_b = 0, 1

        self._registry.add_log(
            "Инициализируем коэффициенты Безу"
            f"- Текущий коэффициент a{current_coefficient_a} \n"
            f"- Следующий коэффициент a{next_coefficient_a}, \n"
            f"- Текущий коэффициент b{current_coefficient_b} \n"
            f"- Следующий коэффициент b{next_coefficient_b}"
        )

        # Шаг 3: Основной цикл расширенного алгоритма Евклида
        while b_abs != 0:
            self._registry.add_log(f"b пока не равен 0, продолжаю цикл, {b=}")
            # Вычисляем частное от деления
            quotient: NumberType = a_abs // b_abs
            self._registry.add_log(f"Вычисляем частное от деления {a_abs=}, {b_abs=}: {quotient=}")

            # Обновляем остаток (a и b меняются местами)
            a_abs, b_abs = b_abs, a_abs % b_abs
            self._registry.add_log(f"Обновляем остатки, a и b меняются местами: {a_abs=}, {b_abs=}")

            # Обновляем коэффициенты Безу для a
            current_coefficient_a, next_coefficient_a = next_coefficient_a, current_coefficient_a - quotient * next_coefficient_a
            self._registry.add_log(
                f"Обновляем коэффициента Безу для a: {current_coefficient_a=}, {next_coefficient_a=}")

            # Обновляем коэффициенты Безу для b
            current_coefficient_b, next_coefficient_b = next_coefficient_b, current_coefficient_b - quotient * next_coefficient_b
            self._registry.add_log(
                f"Обновляем коэффициенты Безу для b: {current_coefficient_b=}, {next_coefficient_b=}")

            self._iterations += 1

        # Шаг 4: Возвращаем результат
        return ResultDTO(
            greatest_common_divisor=a_abs,  # НОД
            x=current_coefficient_a,  # Коэффициент x
            y=current_coefficient_b  # Коэффициент y
        )
