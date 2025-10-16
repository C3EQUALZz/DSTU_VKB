from math import gcd
from typing import List, Optional, Tuple, Final, Iterable, override

from app.core.registry import LogRegistry
from app.exceptions.models.system_of_comprasion_of_the_first_degree import NumberOfResiduesAndModulesMustMatchError, \
    InverseWasNotFoundError
from app.models.system_of_comprasion_of_the_first_degree.base import IChineseRemainderSolver

# Типы для аннотаций
Modulus = int
Remainder = int


class ChineseRemainderSolver(IChineseRemainderSolver):
    def __init__(self) -> None:
        """
        Инициализирует решатель системы сравнений по китайской теореме об остатках.
        Использует `LogRegistry` для записи шагов вычислений.
        """
        self._logger: Final[LogRegistry] = LogRegistry()

    @override
    def solve(
            self,
            remainders: List[Remainder],
            moduli: List[Modulus],
            coefficients: List[int] | None = None
    ) -> Optional[Tuple[Modulus, Modulus]]:
        """
        Решает систему сравнений вида:
        x ≡ a₁ (mod m₁)
        x ≡ a₂ (mod m₂)
        ...
        x ≡ aₙ (mod mₙ)

        Где:
        - Все mᵢ должны быть попарно взаимно простыми.
        - Количество остатков должно совпадать с количеством модулей.

        Возвращает:
            tuple(solution, modulus): Основное решение и общий модуль M.
            None: Если система несовместна.
        """
        # Нормализуем коэффициенты: по умолчанию все равны 1 (x ≡ a_i (mod m_i))
        if coefficients is None:
            coefficients = [1 for _ in remainders]

        # Проверка соответствия длины остатков и модулей и коэффициентов
        if len(remainders) != len(moduli) or len(coefficients) != len(moduli):
            self._logger.add_log("Ошибка: Количество остатков и модулей должно совпадать.")
            return None

        # Проверка попарной взаимной простоты модулей
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if gcd(moduli[i], moduli[j]) != 1:
                    raise NumberOfResiduesAndModulesMustMatchError(f"Модули {moduli[i]} и {moduli[j]} не взаимно просты.")

        # Преобразуем уравнения c_i x ≡ a_i (mod m_i) к виду x ≡ a'_i (mod m'_i)
        # где m'_i = m_i / gcd(c_i, m_i), a'_i = (a_i / gcd) * (c_i/gcd)^{-1} (mod m'_i)
        reduced_remainders: list[int] = []
        reduced_moduli: list[int] = []
        for index, (a_i, m_i, c_i) in enumerate(zip(remainders, moduli, coefficients)):
            d = gcd(c_i, m_i)
            if a_i % d != 0:
                self._logger.add_log(f"Уравнение {index + 1}: {c_i}x ≡ {a_i} (mod {m_i}) несовместно, так как d=gcd({c_i},{m_i})={d} не делит {a_i}.")
                return None
            m_reduced = m_i // d
            a_reduced = (a_i // d)
            c_reduced = (c_i // d) % m_reduced
            inv_c = self._find_modular_inverse(c_reduced % m_reduced, m_reduced)
            if inv_c is None:
                raise InverseWasNotFoundError(f"Обратный элемент для {c_reduced} по модулю {m_reduced} не найден.")
            a_prime = (a_reduced * inv_c) % m_reduced
            reduced_remainders.append(a_prime)
            reduced_moduli.append(m_reduced)
            self._logger.add_log(f"Уравнение {index + 1}: приведено к x ≡ {a_prime} (mod {m_reduced}).")

        # Вычисление общего модуля M
        total_modulus: int = 1
        for modulus in reduced_moduli:
            total_modulus *= modulus
        self._logger.add_log(f"Общий модуль M = {total_modulus}")

        # Вычисление решения
        partial_solutions_sum: int = 0
        for index, (remainder, modulus) in enumerate(zip(reduced_remainders, reduced_moduli)):
            mi: int = total_modulus // modulus
            inv_mi: int = self._find_modular_inverse(mi, modulus)

            if inv_mi is None:
                raise InverseWasNotFoundError(f"Обратный элемент для {mi} по модулю {modulus} не найден.")

            # Логирование промежуточных шагов
            self._logger.add_log(f"M{index + 1} = M / m{index + 1} = {mi}")
            self._logger.add_log(f"Обратный элемент к M{index + 1} по модулю m{index + 1} = {inv_mi}")
            self._logger.add_log(
                f"x{index + 1} = a{index + 1} * M{index + 1} * (M{index + 1}⁻¹) = {remainder * mi * inv_mi}")

            partial_solutions_sum += remainder * mi * inv_mi
            self._logger.add_log(f"x = x + x{index + 1} = {partial_solutions_sum}")

        # Вычисление окончательного решения
        solution = partial_solutions_sum % total_modulus
        self._logger.add_log(f"x = {partial_solutions_sum} % {total_modulus} = {solution}")
        self._logger.add_log(f"Решение системы сравнений: {solution}")

        return solution, total_modulus

    @staticmethod
    def _find_modular_inverse(number: int, modulus: int) -> Optional[int]:
        """
        Находит обратный элемент числа `number` по модулю `modulus` с использованием расширенного алгоритма Евклида.

        Параметры:
            number (int): Число, для которого ищется обратный элемент.
            modulus (int): Модуль, по которому ищется обратный элемент.

        Возвращает:
            int | None: Обратный элемент, если существует, иначе None.
        """
        original_modulus: int = modulus
        x0, x1 = 0, 1

        if modulus == 1:
            return None  # Обратный элемент не существует при m=1

        while number > 1:
            q = number // modulus
            number, modulus = modulus, number % modulus
            x0, x1 = x1 - q * x0, x0

        if x1 < 0:
            x1 += original_modulus

        return x1 if number == 1 else None

    @override
    def get_logs(self) -> Iterable[str]:
        """
        Возвращает логи вычислений для отображения пользователю.

        Returns:
            Iterable[str]: Список строк с пошаговым описанием.
        """
        return self._logger.logs
