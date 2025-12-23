"""Сервис для работы с полиномиальным конгруэнтным генератором."""

from collections import deque
from collections.abc import Iterable
import logging
from math import gcd
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.entities.polynomial_congruent_generator import (
    PolynomialCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.ports.polynomial_congruent_id_generator import (
    PolynomialCongruentIDGenerator,
)


logger: Final[logging.Logger] = logging.getLogger(__name__)


class PolynomialCongruentGeneratorService(DomainService):
    """Сервис для создания и управления полиномиальными конгруэнтными генераторами."""

    def __init__(self, id_generator: PolynomialCongruentIDGenerator) -> None:
        """
        Инициализация сервиса генератором идентификаторов.

        :param id_generator: генератор идентификаторов для полиномиального конгруэнтного генератора
        """
        super().__init__()
        self._id_generator: Final[PolynomialCongruentIDGenerator] = id_generator

    def create(
        self,
        a1: int,
        a2: int,
        b: int,
        x: int,
        m: int,
    ) -> PolynomialCongruentGenerator:
        """
        Создать новый полиномиальный конгруэнтный генератор.

        :param a1: коэффициент a1
        :param a2: коэффициент a2
        :param b: коэффициент b
        :param x: начальное значение x0
        :param m: модуль m
        :return: экземпляр полиномиального конгруэнтного генератора
        """
        logger.info(
            "Создание полиномиального конгруэнтного генератора с параметрами: a1=%s, a2=%s, b=%s, x0=%s, m=%s",
            a1,
            a2,
            b,
            x,
            m,
        )

        generator = PolynomialCongruentGenerator(
            id=self._id_generator(),
            a1=a1,
            a2=a2,
            b=b,
            x=x,
            m=m,
        )

        logger.info("Полиномиальный конгруэнтный генератор успешно создан: %s", generator)
        return generator

    @staticmethod
    def get_random_sequence(
        generator: PolynomialCongruentGenerator,
        count: int,
    ) -> Iterable[int]:
        """
        Сгенерировать последовательность псевдослучайных чисел.

        :param generator: объект генератора
        :param count: количество элементов для генерации
        :return: последовательность сгенерированных чисел
        """
        logger.info(
            "Запуск генерации последовательности полиномиальным конгруэнтным генератором, количество элементов: %s",
            count,
        )

        sequence: deque[int] = deque([generator.x])
        current: int = generator.x

        for index in range(1, count):
            current = generator.next(current)
            sequence.append(current)
            logger.debug("Сгенерирован элемент последовательности #%s: %s", index, current)

        logger.info("Генерация последовательности завершена, всего элементов: %s", len(sequence))
        return sequence

    @staticmethod
    def _get_odd_prime_factors(number: int) -> list[int]:
        """
        Получить список нечетных простых делителей заданного числа.

        :param number: число для разложения на множители
        :return: список уникальных нечетных простых делителей
        """
        factors = []
        # Убираем все двойки
        while number % 2 == 0:
            number //= 2
        
        # Ищем нечетные простые делители
        d = 3
        while d * d <= number:
            if number % d == 0:
                factors.append(d)
                while number % d == 0:
                    number //= d
            d += 2
        
        if number > 2:
            factors.append(number)
        
        return list(set(factors))

    @staticmethod
    def is_maximized_period(
        generator: PolynomialCongruentGenerator,
    ) -> bool:
        """
        Проверить, выполнены ли условия максимального периода (равного m).

        Условия максимального периода для квадратичного конгруэнтного генератора:
        1. gcd(b, m) == 1
        2. Для каждого нечетного простого делителя p числа m:
           (a1 - 1) ≡ 0 (mod p) И a2 ≡ 0 (mod p)
        3. Если a2 четное:
           - Если m делится на 4, то a2 ≡ (a1 - 1) (mod 4)
           - Иначе если m четное, то a2 ≡ (a1 - 1) (mod 2)
        4. a2 mod 9 ≠ (b * 3) mod 9

        :param generator: объект генератора
        :return: ``True``, если все условия выполнены, иначе ``False``
        """
        logger.info(
            "Проверка условия максимального периода для полиномиального генератора: %s",
            generator,
        )

        # Базовая проверка: модуль должен быть больше 1
        if generator.m <= 1:
            logger.info("Условие максимального периода не выполнено: m <= 1")
            return False

        # Проверка диапазона параметров
        if not (0 <= generator.a1 < generator.m):
            logger.info("Условие максимального периода не выполнено: a1 вне допустимого диапазона")
            return False
        if not (0 <= generator.a2 < generator.m):
            logger.info("Условие максимального периода не выполнено: a2 вне допустимого диапазона")
            return False
        if not (0 <= generator.b < generator.m):
            logger.info("Условие максимального периода не выполнено: b вне допустимого диапазона")
            return False
        if not (0 <= generator.x < generator.m):
            logger.info("Условие максимального периода не выполнено: x0 вне допустимого диапазона")
            return False

        # Условие 1: gcd(b, m) == 1
        gcd_bm = gcd(generator.b, generator.m)
        logger.info("Вычислено gcd(b, m): gcd(%s, %s) = %s", generator.b, generator.m, gcd_bm)
        if gcd_bm != 1:
            logger.info("Условие 1 не выполнено: gcd(b, m) != 1")
            return False

        # Условие 2: для каждого нечетного простого делителя p числа m
        odd_prime_factors = PolynomialCongruentGeneratorService._get_odd_prime_factors(generator.m)
        logger.info("Нечетные простые делители m=%s: %s", generator.m, odd_prime_factors)
        
        for p in odd_prime_factors:
            a1_minus_1_mod_p = (generator.a1 - 1) % p
            a2_mod_p = generator.a2 % p
            logger.info(
                "Проверка для p=%s: (a1 - 1) mod %s = %s, a2 mod %s = %s",
                p, p, a1_minus_1_mod_p, p, a2_mod_p
            )
            if not (a1_minus_1_mod_p == 0 and a2_mod_p == 0):
                logger.info("Условие 2 не выполнено для простого делителя p=%s", p)
                return False

        a2_mod_2 = generator.a2 % 2
        if a2_mod_2 != 0:
            logger.info("Условие 3 не выполнено: a2 нечетное")
            return False

        m_mod_4 = generator.m % 4
        m_mod_2 = generator.m % 2
        a2_mod_4 = generator.a2 % 4
        a1_minus_1_mod_4 = (generator.a1 - 1) % 4
        a1_minus_1_mod_2 = (generator.a1 - 1) % 2

        if not (m_mod_4 == 0 and a2_mod_4 == a1_minus_1_mod_4):
            logger.info("Условие 3 не выполнено")
            return False
        elif not (m_mod_2 == 0 and a2_mod_2 == a1_minus_1_mod_2):
            logger.info("Условие 3 не выполнено")
            return False

        a2_mod_9 = generator.a2 % 9
        b_times_3_mod_9 = (generator.b * 3) % 9
        logger.debug(
            "Проверка условия 4: a2 mod 9 = %s, (b * 3) mod 9 = %s",
            a2_mod_9, b_times_3_mod_9
        )
        if a2_mod_9 == b_times_3_mod_9:
            logger.info("Условие 4 не выполнено: a2 mod 9 == (b * 3) mod 9")
            return False

        logger.info("Все условия максимального периода выполнены")
        return True

    @staticmethod
    def check_max_period_conditions_detailed(
        generator: PolynomialCongruentGenerator,
    ) -> tuple[bool, list[tuple[int, str, bool, str]]]:
        """
        Проверить условия максимального периода и вернуть детальную информацию.

        :param generator: объект генератора
        :return: кортеж (все_условия_выполнены, список_результатов_проверки)
                 где каждый элемент списка - (номер_условия, описание, выполнено, детали)
        """
        conditions_results: list[tuple[int, str, bool, str]] = []
        all_fulfilled = True

        # Базовая проверка: модуль должен быть больше 1
        if generator.m <= 1:
            conditions_results.append((0, "m > 1", False, f"m = {generator.m} <= 1"))
            return False, conditions_results

        # Проверка диапазона параметров
        if not (0 <= generator.a1 < generator.m):
            conditions_results.append((0, "0 <= a1 < m", False, f"a1 = {generator.a1} вне диапазона"))
            return False, conditions_results
        if not (0 <= generator.a2 < generator.m):
            conditions_results.append((0, "0 <= a2 < m", False, f"a2 = {generator.a2} вне диапазона"))
            return False, conditions_results
        if not (0 <= generator.b < generator.m):
            conditions_results.append((0, "0 <= b < m", False, f"b = {generator.b} вне диапазона"))
            return False, conditions_results
        if not (0 <= generator.x < generator.m):
            conditions_results.append((0, "0 <= x0 < m", False, f"x0 = {generator.x} вне диапазона"))
            return False, conditions_results

        # Условие 1: gcd(b, m) == 1
        gcd_bm = gcd(generator.b, generator.m)
        condition1_fulfilled = gcd_bm == 1
        condition1_details = f"gcd({generator.b}, {generator.m}) = {gcd_bm}"
        conditions_results.append((1, "gcd(b, m) = 1", condition1_fulfilled, condition1_details))
        if not condition1_fulfilled:
            all_fulfilled = False

        # Условие 2: для каждого нечетного простого делителя p числа m
        odd_prime_factors = PolynomialCongruentGeneratorService._get_odd_prime_factors(generator.m)
        condition2_fulfilled = True
        condition2_details_parts = []
        
        if not odd_prime_factors:
            condition2_details = "у m нет нечетных простых делителей"
        else:
            for p in odd_prime_factors:
                a1_minus_1_mod_p = (generator.a1 - 1) % p
                a2_mod_p = generator.a2 % p
                if not (a1_minus_1_mod_p == 0 and a2_mod_p == 0):
                    condition2_fulfilled = False
                    condition2_details_parts.append(
                        f"для p={p}: (a1-1) mod {p}={a1_minus_1_mod_p}, a2 mod {p}={a2_mod_p}"
                    )
            
            if condition2_fulfilled:
                condition2_details = f"для всех нечетных простых делителей p={odd_prime_factors}: (a1-1) ≡ 0 (mod p) и a2 ≡ 0 (mod p)"
            else:
                condition2_details = "; ".join(condition2_details_parts)
        
        condition2_description = (
            "у m нет нечетных простых делителей" if not odd_prime_factors
            else "Для каждого нечетного простого делителя p: (a1-1) ≡ 0 (mod p) и a2 ≡ 0 (mod p)"
        )
        conditions_results.append((
            2,
            condition2_description,
            condition2_fulfilled,
            condition2_details
        ))
        if not condition2_fulfilled:
            all_fulfilled = False

        # Условие 3: проверка четности
        a2_mod_2 = generator.a2 % 2
        m_mod_4 = generator.m % 4
        m_mod_2 = generator.m % 2
        a2_mod_4 = generator.a2 % 4
        a1_minus_1_mod_4 = (generator.a1 - 1) % 4
        a1_minus_1_mod_2 = (generator.a1 - 1) % 2
        
        condition3_fulfilled = True
        condition3_details = ""
        
        if a2_mod_2 != 0:
            condition3_fulfilled = False
            condition3_details = f"a2 = {generator.a2} нечетное"
        elif m_mod_4 == 0:
            if a2_mod_4 == a1_minus_1_mod_4:
                condition3_details = f"m кратно 4, a2 четное и a2 ≡ (a1-1) (mod 4): {a2_mod_4} ≡ {a1_minus_1_mod_4}"
            else:
                condition3_fulfilled = False
                condition3_details = f"m кратно 4, но a2 mod 4 = {a2_mod_4} ≠ (a1-1) mod 4 = {a1_minus_1_mod_4}"
        elif m_mod_2 == 0:
            if a2_mod_2 == a1_minus_1_mod_2:
                condition3_details = f"m четное, a2 четное и a2 ≡ (a1-1) (mod 2): {a2_mod_2} ≡ {a1_minus_1_mod_2}"
            else:
                condition3_fulfilled = False
                condition3_details = f"m четное, но a2 mod 2 = {a2_mod_2} ≠ (a1-1) mod 2 = {a1_minus_1_mod_2}"
        else:
            # m нечетное
            condition3_fulfilled = False
            condition3_details = f"m = {generator.m} нечетное, условие не применимо"
        
        conditions_results.append((
            3,
            "m кратно 4, a2 четное и a2 ≡ (a1-1) (mod 4); или m четное, a2 четное и a2 ≡ (a1-1) (mod 2)",
            condition3_fulfilled,
            condition3_details
        ))
        if not condition3_fulfilled:
            all_fulfilled = False

        # Условие 4: a2 mod 9 != (b * 3) mod 9
        a2_mod_9 = generator.a2 % 9
        b_times_3_mod_9 = (generator.b * 3) % 9
        condition4_fulfilled = a2_mod_9 != b_times_3_mod_9
        condition4_details = f"a2 mod 9 = {a2_mod_9}, (b*3) mod 9 = {b_times_3_mod_9}"
        conditions_results.append((
            4,
            "a2 mod 9 ≠ (b * 3) mod 9",
            condition4_fulfilled,
            condition4_details
        ))
        if not condition4_fulfilled:
            all_fulfilled = False

        return all_fulfilled, conditions_results

    @staticmethod
    def get_period(
        generator: PolynomialCongruentGenerator,
    ) -> int:
        """
        Определить длину периода последовательности с помощью алгоритма
        обнаружения цикла Флойда.

        :param generator: объект генератора
        :return: длина периода
        """
        logger.info(
            "Вычисление длины периода для полиномиального конгруэнтного генератора: %s",
            generator,
        )

        # Алгоритм обнаружения цикла Флойда (метод «черепаха и заяц»)
        turtle = generator.next(generator.x)
        hare = generator.next(generator.next(generator.x))
        logger.debug("Начальные значения алгоритма Флойда: черепаха=%s, заяц=%s", turtle, hare)

        # Поиск точки встречи
        steps_to_meet = 0
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(generator.next(hare))
            steps_to_meet += 1
        logger.debug("Найдена точка встречи после %s шагов: значение=%s", steps_to_meet, turtle)

        # Поиск начала цикла
        turtle = generator.x
        steps_to_start = 0
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(hare)
            steps_to_start += 1
        logger.debug("Начало цикла найдено через %s шагов от x0", steps_to_start)

        # Измерение длины периода
        hare = generator.next(turtle)
        period = 1
        while turtle != hare:
            hare = generator.next(hare)
            period += 1

        logger.info("Длина периода последовательности: %s", period)
        return period

    @staticmethod
    def get_start_period_index(
        generator: PolynomialCongruentGenerator,
    ) -> int:
        """
        Определить индекс, с которого начинается период последовательности.

        :param generator: объект генератора
        :return: индекс начала периода
        """
        logger.info(
            "Вычисление индекса начала периода для полиномиального конгруэнтного генератора: %s",
            generator,
        )

        # Алгоритм обнаружения цикла Флойда (поиск точки встречи)
        turtle = generator.next(generator.x)
        hare = generator.next(generator.next(generator.x))

        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(generator.next(hare))

        # Поиск начала цикла
        turtle = generator.x
        start = 0
        while turtle != hare:
            turtle = generator.next(turtle)
            hare = generator.next(hare)
            start += 1

        logger.info("Индекс начала периода: %s", start)
        return start




