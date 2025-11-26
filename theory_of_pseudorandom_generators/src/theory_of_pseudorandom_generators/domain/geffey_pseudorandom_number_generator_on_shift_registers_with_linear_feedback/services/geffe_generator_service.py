"""Service for working with Geffe generator."""

import logging
from collections.abc import Iterable
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.geffe_generator import (
    GeffeGenerator,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.ports.geffe_generator_id_generator import (
    GeffeGeneratorIDGenerator,
)


class GeffeGeneratorService(DomainService):
    """Service for creating and managing Geffe generators."""

    def __init__(self, id_generator: GeffeGeneratorIDGenerator) -> None:
        """Initialize service with ID generator.

        Args:
            id_generator: Generator for creating Geffe generator IDs
        """
        super().__init__()
        self._id_generator: Final[GeffeGeneratorIDGenerator] = id_generator

    def create(
        self,
        register1: Register,
        register2: Register,
        register3: Register,
    ) -> GeffeGenerator:
        """Create a new Geffe generator.

        Args:
            register1: First LFSR register
            register2: Second LFSR register
            register3: Third LFSR register

        Returns:
            New Geffe generator instance
        """
        return GeffeGenerator(
            id=self._id_generator(),
            register1=register1,
            register2=register2,
            register3=register3,
        )

    @staticmethod
    def get_states(
        generator: GeffeGenerator,
        separator: str = " -> ",
    ) -> Iterable[str]:
        """Generate state strings for all period states.

        Args:
            generator: Geffe generator to generate from
            separator: Separator between state and result

        Yields:
            Formatted state strings
        """
        generator.clear()
        for i in range(generator.period):
            arr = generator.next_array()
            # Calculate result using Geffe formula
            x1, x2, x3 = arr[0], arr[1], arr[2]
            result = ((x1 & x2) + (x2 & x3)) % 2
            result = (result + x3) % 2
            state_str = "".join(str(v) for v in arr)
            yield f"{i}. {state_str}{separator}{result}"

    @staticmethod
    def get_decimal_sequence(
        generator: GeffeGenerator,
        number_count: int,
    ) -> str:
        """Convert binary sequence to decimal numbers.

        Использует фиксированный размер блока 9 бит для перевода в десятичную систему.
        Это соответствует максимальному значению 511 (2^9 - 1).
        Последовательность генерируется циклически, пока не наберется нужное количество чисел.

        Args:
            generator: Geffe generator to generate from
            number_count: Number of decimal numbers to generate

        Returns:
            Tab-separated decimal sequence
        """
        logger.info("Запрошено чисел для перевода в 10-ную систему: %s", number_count)
        logger.info("Период генератора: %s", generator.period)
        
        # Используем фиксированный размер блока 9 бит (максимальное значение 511)
        bit_block_size = 9
        required_bits = number_count * bit_block_size
        
        # Генерируем биты циклически, пока не наберется нужное количество
        generator.clear()
        binary_sequence: list[str] = []
        
        logger.info("Начинаем генерацию %s бит (требуется для %s чисел по %s бит)", required_bits, number_count, bit_block_size)
        
        # Генерируем биты напрямую, циклически используя генератор
        bits_generated = 0
        for i in range(required_bits):
            try:
                bit = generator.next_bit()
                binary_sequence.append(str(bit))
                bits_generated += 1
                if i < 10 or (i % 100 == 0):  # Логируем первые 10 и каждые 100
                    logger.debug("Сгенерирован бит %s: %s", i, bit)
            except Exception as e:
                logger.error("Ошибка при генерации бита %s: %s", i, e)
                break
        
        sequence = "".join(binary_sequence)
        logger.info("Сгенерировано бинарных бит: %s (ожидалось %s)", len(sequence), required_bits)
        
        if len(sequence) < required_bits:
            logger.warning(
                (
                    "Сгенерировано меньше бит, чем требуется! "
                    "Сгенерировано: %s, требуется: %s. "
                    "Будет сгенерировано меньше чисел."
                ),
                len(sequence),
                required_bits,
            )

        decimal_numbers: list[str] = []
        actual_count = min(number_count, len(sequence) // bit_block_size)
        logger.info("Будет сгенерировано чисел: %s (из запрошенных %s)", actual_count, number_count)
        
        for i in range(actual_count):
            start_index = i * bit_block_size
            end_index = start_index + bit_block_size
            
            # Берем блок из 9 бит
            binary_str = sequence[start_index:end_index]
            
            if not binary_str or len(binary_str) < bit_block_size:
                # Если блок короче 9 бит, дополняем нулями справа
                if binary_str:
                    binary_str = binary_str + "0" * (bit_block_size - len(binary_str))
                else:
                    binary_str = "0" * bit_block_size
                logger.debug("Блок %s короче 9 бит, дополнен нулями: %s", i, binary_str)
                
            # Переводим в десятичную систему
            decimal_num = int(binary_str, 2) if binary_str else 0
            decimal_numbers.append(str(decimal_num))
            
            if i < 5:  # Логируем первые 5 для отладки
                logger.debug("Блок %s: бинарная строка '%s' -> десятичное %s", i, binary_str, decimal_num)

        logger.info("Сгенерировано десятичных чисел: %s", len(decimal_numbers))
        return "\t".join(decimal_numbers)
