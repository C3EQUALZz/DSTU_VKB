import logging
from collections import deque
from collections.abc import Iterable
from math import gcd
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.entities.linear_congruent_generator import (
    LinearCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.ports.linear_congruent_id_generator import (
    LinearCongruentIDGenerator,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class LinearCongruentGeneratorService(DomainService):
    def __init__(self, id_generator: LinearCongruentIDGenerator) -> None:
        super().__init__()
        self._id_generator: Final[LinearCongruentIDGenerator] = id_generator

    def create(
        self,
        a: int,
        b: int,
        x: int,
        m: int,
    ) -> LinearCongruentGenerator:
        """
        Создать новый линейный конгруэнтный генератор.

        :param a: множитель (коэффициент a)
        :param b: приращение (коэффициент b)
        :param x: начальное значение (x0)
        :param m: модуль (m)
        :return: экземпляр линейного конгруэнтного генератора
        """
        logger.info(
            "Создание линейного конгруэнтного генератора с параметрами: a=%s, b=%s, x0=%s, m=%s",
            a,
            b,
            x,
            m,
        )

        new_entity = LinearCongruentGenerator(
            id=self._id_generator(),
            a=a,
            b=b,
            x=x,
            m=m,
        )

        logger.info("Линейный конгруэнтный генератор успешно создан: %s", new_entity)

        return new_entity

    # noinspection PyMethodMayBeStatic
    def get_random_sequence(
        self,
        generator: LinearCongruentGenerator,
        count: int,
    ) -> Iterable[int]:
        """
        Сгенерировать последовательность псевдослучайных чисел.

        :param generator: объект генератора
        :param count: количество элементов последовательности
        :return: сгенерированная последовательность чисел
        """
        logger.info(
            "Запуск генерации последовательности псевдослучайных чисел, количество элементов: %s",
            count,
        )
        sequence: deque[int] = deque([generator.x])
        current: int = generator.x
        logger.info("Начальный элемент последовательности: %s", current)

        for index in range(1, count):
            current = generator.next(current)
            sequence.append(current)
            logger.debug(
                "Сгенерирован элемент последовательности #%s: %s", index, current
            )

        logger.info("Генерация последовательности завершена, всего элементов: %s", len(sequence))

        return sequence

    # noinspection PyMethodMayBeStatic
    def is_maximized_period(
        self,
        generator: LinearCongruentGenerator,
    ) -> bool:
        """
        Проверить, имеет ли генератор максимальный период (равный m).

        :param generator: объект генератора
        :return: ``True``, если период максимальный, иначе ``False``
        """
        logger.info(
            "Проверка условия максимального периода для генератора: %s", generator
        )

        # Проверка условия gcd(b, m) == 1
        gcd_value = gcd(generator.b, generator.m)
        logger.debug("Вычислено gcd(b, m): gcd(%s, %s) = %s", generator.b, generator.m, gcd_value)
        if gcd_value != 1:
            logger.info("Условие максимального периода не выполнено: gcd(b, m) != 1")
            return False

        # Получение множителей числа m (включая 1)
        multipliers = self.__get_multipliers_list(generator.m)
        logger.debug("Множители числа m=%s: %s", generator.m, multipliers)

        # Проверка делимости (a - 1) на все множители
        if any((generator.a - 1) % x != 0 for x in multipliers):
            logger.info(
                "Условие максимального периода не выполнено: (a - 1) не делится на все множители m"
            )
            return False

        # Проверка делимости m на 4
        if generator.m % 4 != 0:
            logger.info("Условие максимального периода не выполнено: m не делится на 4")
            return False

        # Проверка, что для всех множителей выполняется (x - 1) % 4 == 0
        if not all((x - 1) % 4 == 0 for x in multipliers):
            logger.info(
                "Условие максимального периода не выполнено: не для всех множителей выполняется (x - 1) % 4 == 0"
            )
            return False

        logger.info("Все условия максимального периода выполнены")
        return True

    def check_max_period_conditions_detailed(
        self,
        generator: LinearCongruentGenerator,
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
        if not (0 <= generator.a < generator.m):
            conditions_results.append((0, "0 <= a < m", False, f"a = {generator.a} вне диапазона"))
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

        # Условие 2: (a - 1) делится на все множители m
        multipliers = self.__get_multipliers_list(generator.m)
        condition2_fulfilled = True
        condition2_failed_multipliers = []
        
        for mult in multipliers:
            if (generator.a - 1) % mult != 0:
                condition2_fulfilled = False
                condition2_failed_multipliers.append(mult)
        
        if condition2_fulfilled:
            condition2_details = f"(a - 1) = {generator.a - 1} делится на все множители m: {multipliers}"
        else:
            condition2_details = f"(a - 1) = {generator.a - 1} не делится на множители: {condition2_failed_multipliers}"
        
        conditions_results.append((
            2,
            "(a - 1) делится на все множители m",
            condition2_fulfilled,
            condition2_details
        ))
        if not condition2_fulfilled:
            all_fulfilled = False

        # Условие 3: m делится на 4
        m_mod_4 = generator.m % 4
        condition3_fulfilled = m_mod_4 == 0
        condition3_details = f"m mod 4 = {m_mod_4}" + (" (m делится на 4)" if condition3_fulfilled else " (m не делится на 4)")
        conditions_results.append((
            3,
            "m делится на 4",
            condition3_fulfilled,
            condition3_details
        ))
        if not condition3_fulfilled:
            all_fulfilled = False

        # Условие 4: для всех множителей выполняется (x - 1) % 4 == 0
        condition4_fulfilled = True
        condition4_failed_multipliers = []
        
        for mult in multipliers:
            if (mult - 1) % 4 != 0:
                condition4_fulfilled = False
                condition4_failed_multipliers.append(mult)
        
        if condition4_fulfilled:
            condition4_details = f"для всех множителей {multipliers}: (x - 1) % 4 == 0"
        else:
            condition4_details = f"для множителей {condition4_failed_multipliers}: (x - 1) % 4 != 0"
        
        conditions_results.append((
            4,
            "Для всех множителей m: (x - 1) % 4 == 0",
            condition4_fulfilled,
            condition4_details
        ))
        if not condition4_fulfilled:
            all_fulfilled = False

        return all_fulfilled, conditions_results

    def get_period(
        self,
        generator: LinearCongruentGenerator,
    ) -> int:
        """
        Определить длину периода последовательности при помощи алгоритма
        обнаружения цикла Флойда.

        :param generator: объект генератора
        :return: длина периода
        """
        logger.info("Вычисление длины периода последовательности для генератора: %s", generator)

        if self.is_maximized_period(generator):
            logger.info("Генератор имеет максимальный период, длина периода равна m=%s", generator.m)
            return generator.m

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

    # noinspection PyMethodMayBeStatic
    def get_start_period_index(
        self,
        generator: LinearCongruentGenerator,
    ) -> int:
        """
        Определить индекс, с которого начинается период последовательности.

        :param generator: объект генератора
        :return: индекс начала периода
        """
        logger.info(
            "Вычисление индекса начала периода последовательности для генератора: %s",
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

    @staticmethod
    def __get_multipliers_list(number: int) -> list[int]:
        """
        Получить список простых множителей заданного числа.

        :param number: число для разложения на множители
        :return: список простых множителей (включая 1)

        Пример:
            __get_multipliers_list(12) -> [1, 2, 2, 3]
        """
        logger.debug("Вычисление множителей числа: %s", number)

        if number == 0:
            logger.debug("Число равно 0, возвращаю [0]")
            return [0]

        multipliers: list[int] = [1]
        divider = 2

        while number != 1:
            if number % divider != 0:
                divider += 1
                continue
            number //= divider
            multipliers.append(divider)

        logger.debug("Найденные множители: %s", multipliers)
        return multipliers


