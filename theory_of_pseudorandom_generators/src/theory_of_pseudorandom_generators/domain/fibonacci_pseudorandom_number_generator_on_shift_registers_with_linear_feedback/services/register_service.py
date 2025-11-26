"""Сервис для работы с регистром Фибоначчи."""

from collections.abc import Iterable, Sequence
import logging
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.register_id_generator import (
    RegisterIDGenerator,
)


logger: Final[logging.Logger] = logging.getLogger(__name__)


class RegisterService(DomainService):
    """Сервис для создания и управления регистрами Фибоначчи."""

    def __init__(self, id_generator: RegisterIDGenerator) -> None:
        """
        Инициализация сервиса генератором идентификаторов.

        :param id_generator: генератор идентификаторов для регистров
        """
        super().__init__()
        self._id_generator: Final[RegisterIDGenerator] = id_generator

    def create(
        self,
        polynomial_coefficients: Sequence[int],
        start_position: Sequence[int],
        shift: int,
        column_index: int = 0,
    ) -> Register:
        """
        Создать новый регистр Фибоначчи.

        :param polynomial_coefficients: коэффициенты примитивного полинома
        :param start_position: начальное состояние регистра
        :param shift: сдвиг (значение k)
        :param column_index: индекс колонки для вывода
        :return: новый экземпляр регистра
        """
        logger.info(
            "Создание регистра Фибоначчи с параметрами: коэффициенты=%s, стартовая позиция=%s, "
            "сдвиг=%s, индекс колонки=%s",
            list(polynomial_coefficients),
            list(start_position),
            shift,
            column_index,
        )

        register = Register(
            id=self._id_generator(),
            polynomial_coefficients=polynomial_coefficients,
            start_position=start_position,
            shift=shift,
            column_index=column_index,
        )

        logger.info("Регистр Фибоначчи успешно создан: %s", register)
        return register

    @staticmethod
    def get_sequence(register: Register, count: int | None = None) -> Iterable[Sequence[int]]:
        """
        Сгенерировать последовательность состояний регистра.

        :param register: регистр, из которого производится генерация
        :param count: количество состояний для генерации (``None`` — полный период)
        :yield: состояния регистра
        """
        logger.info(
            "Генерация последовательности состояний регистра. Количество состояний: %s",
            "полный период" if count is None else count,
        )

        register.clear()
        if count is None:
            # Генерируем полный период (логика согласована с Java-реализацией)
            # Начинаем с первого next() (не с начального состояния)
            start_state = list(register.start_position)
            current = register.next()
            yield current
            current = register.next()
            while list(register._register[0]) != start_state:
                yield current
                current = register.next()
            # Последнее состояние (равное start_state) здесь не возвращается;
            # оно будет преобразовано в десятичный вид в get_decimal_sequence
        else:
            for _ in range(count):
                yield register.next()

    @staticmethod
    def get_binary_sequence(register: Register, count: int | None = None) -> Iterable[str]:
        """
        Сгенерировать бинарную последовательность по состояниям регистра.

        :param register: регистр, из которого производится генерация
        :param count: количество состояний для генерации (``None`` — полный период)
        :yield: строковые бинарные представления состояний регистра
        """
        logger.info(
            "Генерация бинарной последовательности из регистра. Количество состояний: %s",
            "полный период" if count is None else count,
        )

        for state in RegisterService.get_sequence(register, count):
            yield "".join(str(bit) for bit in state)

    @staticmethod
    def get_decimal_sequence(register: Register, count: int | None = None) -> Iterable[int]:
        """
        Сгенерировать десятичную последовательность по бинарным состояниям регистра.

        :param register: регистр, из которого производится генерация
        :param count: количество состояний для генерации (``None`` — полный период)
        :yield: десятичные числа, полученные из бинарных состояний
        """
        logger.info(
            "Генерация десятичной последовательности из регистра. Количество состояний: %s",
            "полный период" if count is None else count,
        )

        for binary_str in RegisterService.get_binary_sequence(register, count):
            yield int(binary_str, 2)

    @staticmethod
    def is_maximized_period(register: Register) -> bool:
        """
        Проверить, имеет ли регистр максимальный период.

        :param register: регистр для проверки
        :return: ``True``, если период максимален (\\(2^n - 1\\)), иначе ``False``
        """
        period = register.get_period()
        is_max = period == register.max_period

        logger.info(
            "Проверка максимального периода регистра. Вычисленный период: %s, максимальный период: %s, результат: %s",
            period,
            register.max_period,
            is_max,
        )

        return is_max

