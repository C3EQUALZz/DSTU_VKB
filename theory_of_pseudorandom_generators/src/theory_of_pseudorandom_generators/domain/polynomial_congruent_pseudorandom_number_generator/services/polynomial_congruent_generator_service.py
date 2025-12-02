"""Сервис для работы с полиномиальным конгруэнтным генератором."""

from collections import deque
from collections.abc import Iterable
import logging
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
    def is_maximized_period(
        generator: PolynomialCongruentGenerator,
    ) -> bool:
        """
        Выполнена ли (упрощённая) проверка на максимально возможный период (m).

        Важно: это **упрощённая** проверка. Полные условия максимального периода
        для квадратичных (полиномиальных) конгруэнтных генераторов значительно сложнее,
        чем для линейных, и зависят от простых множителей модуля m.

        :param generator: объект генератора
        :return: ``True``, если базовые условия выполнены, иначе ``False``
        """
        logger.info(
            "Проверка (упрощённого) условия максимального периода для полиномиального генератора: %s",
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

        logger.info(
            "Базовые условия для потенциально максимального периода выполнены. "
            "Точная длина периода будет вычислена функцией get_period().",
        )
        return True

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



