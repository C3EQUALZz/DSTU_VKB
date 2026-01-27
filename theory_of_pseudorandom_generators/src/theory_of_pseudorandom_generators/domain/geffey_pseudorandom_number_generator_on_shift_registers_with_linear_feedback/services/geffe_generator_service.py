"""Service for working with Geffe generator."""

import logging
from collections.abc import Iterable, Sequence
from typing import Final

from theory_of_pseudorandom_generators.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.services.register_service import (
    RegisterService,
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
    def get_register_sequences(
        generator: GeffeGenerator,
        register_service: RegisterService,
    ) -> tuple[list[int], list[int], list[int]]:
        """Generate sequences and then decimate them (classic Geffe setup).

        Steps:
        1. Generate sequences using ordinary shift (k=1) for all registers
           until the combined state repeats.
        2. Apply decimation seq[::k] for each register's k.
        """
        seq1_full: list[int] = []
        seq2_full: list[int] = []
        seq3_full: list[int] = []
        col1 = generator.register1.column_index
        col2 = generator.register2.column_index
        col3 = generator.register3.column_index
        for _, state1, state2, state3 in GeffeGeneratorService._iter_combined_states(
            generator, register_service
        ):
            seq1_full.append(state1[col1])
            seq2_full.append(state2[col2])
            seq3_full.append(state3[col3])

        k1 = generator.register1.shift
        k2 = generator.register2.shift
        k3 = generator.register3.shift

        decimated1 = seq1_full[::k1]
        decimated2 = seq2_full[::k2]
        decimated3 = seq3_full[::k3]

        return decimated1, decimated2, decimated3

    @staticmethod
    def get_steps(
        generator: GeffeGenerator,
        register_service: RegisterService,
        steps_limit: int | None = None,
    ) -> list[str]:
        """Generate step-by-step output strings for combined states."""
        steps: list[str] = []
        col1 = generator.register1.column_index
        col2 = generator.register2.column_index
        col3 = generator.register3.column_index
        for step, state1, state2, state3 in GeffeGeneratorService._iter_combined_states(
            generator, register_service
        ):
            x1 = state1[col1]
            x2 = state2[col2]
            x3 = state3[col3]
            step_lines = [
                f"Шаг {step}:",
                (
                    f"  LFSR1: {''.join(str(b) for b in state1)} -> "
                    f"выбранный бит (столбец {col1 + 1}): {x1}"
                ),
                (
                    f"  LFSR2: {''.join(str(b) for b in state2)} -> "
                    f"выбранный бит (столбец {col2 + 1}): {x2}"
                ),
                (
                    f"  LFSR3: {''.join(str(b) for b in state3)} -> "
                    f"выбранный бит (столбец {col3 + 1}): {x3}"
                ),
                f"  f(x1,x2,x3) = {GeffeGeneratorService._geffe_bit(x1, x2, x3)}",
            ]
            steps.append("\n".join(step_lines))
            if steps_limit is not None and steps_limit > 0 and step + 1 >= steps_limit:
                break
        return steps

    @staticmethod
    def get_final_sequence(
        seq1: Sequence[int],
        seq2: Sequence[int],
        seq3: Sequence[int],
        length: int | None = None,
    ) -> list[int]:
        """Combine three sequences using Geffe formula.

        If length is provided, sequences are repeated to match that length.
        Otherwise, the minimum length is used.
        """
        if not seq1 or not seq2 or not seq3:
            return []
        if length is None:
            length = min(len(seq1), len(seq2), len(seq3))
        final_sequence: list[int] = []
        for i in range(length):
            x1 = seq1[i % len(seq1)]
            x2 = seq2[i % len(seq2)]
            x3 = seq3[i % len(seq3)]
            result = GeffeGeneratorService._geffe_bit(x1, x2, x3)
            final_sequence.append(result)
        return final_sequence

    @staticmethod
    def get_decimal_sequence_from_bits(
        bit_sequence: Sequence[int],
        number_count: int,
        bit_block_size: int = 16,
    ) -> str:
        """Convert bit sequence into decimal numbers using fixed-size blocks."""
        if number_count <= 0 or not bit_sequence:
            return ""
        required_bits = number_count * bit_block_size
        bits = [str(bit_sequence[i % len(bit_sequence)]) for i in range(required_bits)]
        sequence = "".join(bits)
        decimal_numbers = [
            str(int(sequence[i : i + bit_block_size], 2))
            for i in range(0, required_bits, bit_block_size)
        ]
        return "\t".join(decimal_numbers)

    @staticmethod
    def binary_to_decimal_str(bit_sequence: Sequence[int]) -> str:
        """Convert a binary bit sequence to a decimal string."""
        if not bit_sequence:
            return "0"
        base = 1_000_000_000
        digits = [0]
        for bit in bit_sequence:
            carry = bit
            for i in range(len(digits)):
                value = digits[i] * 2 + carry
                digits[i] = value % base
                carry = value // base
            if carry:
                digits.append(carry)
        parts = [str(digits[-1])]
        for digit in reversed(digits[:-1]):
            parts.append(f"{digit:09d}")
        return "".join(parts)

    @staticmethod
    def _geffe_bit(x1: int, x2: int, x3: int) -> int:
        """Calculate one Geffe output bit."""
        return (x1 & x2) ^ (x2 & x3) ^ x3

    @staticmethod
    def _iter_combined_states(
        generator: GeffeGenerator,
        register_service: RegisterService,
    ) -> Iterable[tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]]:
        """Yield combined register states using shift=1 until repetition."""
        temp_register1 = register_service.create(
            polynomial_coefficients=generator.register1.polynomial_coefficients,
            start_position=generator.register1.start_position,
            shift=1,
            column_index=generator.register1.column_index,
        )
        temp_register2 = register_service.create(
            polynomial_coefficients=generator.register2.polynomial_coefficients,
            start_position=generator.register2.start_position,
            shift=1,
            column_index=generator.register2.column_index,
        )
        temp_register3 = register_service.create(
            polynomial_coefficients=generator.register3.polynomial_coefficients,
            start_position=generator.register3.start_position,
            shift=1,
            column_index=generator.register3.column_index,
        )

        seen_states: set[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]] = set()

        temp_register1.clear()
        temp_register2.clear()
        temp_register3.clear()

        step = 0
        while True:
            state1 = tuple(temp_register1.next())
            state2 = tuple(temp_register2.next())
            state3 = tuple(temp_register3.next())
            combined_state = (state1, state2, state3)
            if combined_state in seen_states:
                break
            seen_states.add(combined_state)
            yield step, state1, state2, state3
            step += 1
    
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
            x1, x2, x3 = arr[0], arr[1], arr[2]
            result = GeffeGeneratorService._geffe_bit(x1, x2, x3)
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
        
        # Используем фиксированный размер блока 16 бит (максимальное значение 65535)
        bit_block_size = 16
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
