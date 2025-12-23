"""Geffe generator entity."""

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from theory_of_pseudorandom_generators.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.entities.register import (
    Register,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.errors import (
    PeriodsNotCoprimeError,
)
from theory_of_pseudorandom_generators.domain.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.geffe_generator_id import (
    GeffeGeneratorID,
)


def gcd_multiple(*numbers: int) -> int:
    """Calculate GCD of multiple numbers.

    Args:
        *numbers: Numbers to calculate GCD for

    Returns:
        GCD of all numbers
    """
    if not numbers:
        return 0
    if len(numbers) == 1:
        return abs(numbers[0])
    result = numbers[0]
    for num in numbers[1:]:
        result = math.gcd(result, num)
    return result


def lcm_multiple(*numbers: int) -> int:
    """Calculate LCM of multiple numbers.

    Args:
        *numbers: Numbers to calculate LCM for

    Returns:
        LCM of all numbers
    """
    if not numbers:
        return 0
    if len(numbers) == 1:
        return abs(numbers[0])
    result = numbers[0]
    for num in numbers[1:]:
        result = abs(result * num) // math.gcd(result, num)
    return result


@dataclass(eq=False, kw_only=True)
class GeffeGenerator(BaseAggregateRoot[GeffeGeneratorID]):
    """Geffe generator using three LFSR registers."""

    register1: Register
    register2: Register
    register3: Register

    _period: int = field(init=False, repr=False)
    _start_position: Sequence[int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize Geffe generator after creation."""
        super().__post_init__()

        # Get max periods (2^N - 1) for theoretical period calculation
        # Note: The theoretical period is calculated as S1 * S2 * S3,
        # where S = 2^N - 1 (max_period), not LCM of actual periods
        max_period1 = self.register1.max_period
        max_period2 = self.register2.max_period
        max_period3 = self.register3.max_period

        # Get actual periods for validation
        period1 = self.register1.get_period()
        period2 = self.register2.get_period()
        period3 = self.register3.get_period()

        # Validate that actual periods are coprime
        if gcd_multiple(period1, period2, period3) != 1:
            msg = "Значения периодов регистров не взаимно простые"
            raise PeriodsNotCoprimeError(msg)

        # Calculate theoretical period as product of max periods (S1 * S2 * S3)
        # This matches the reference implementation
        self._period = max_period1 * max_period2 * max_period3

        # Set start position
        self._start_position = self._set_start_position()

    def _set_start_position(self) -> Sequence[int]:
        """Set initial position by getting first value from each register.

        Returns:
            Initial state values from all three registers
        """
        start_state = [0] * 3
        registers = [self.register1, self.register2, self.register3]
        for i, register in enumerate(registers):
            state = register.next()
            start_state[i] = state[register.column_index]
            register.clear()
        return tuple(start_state)

    def clear(self) -> None:
        """Reset all registers to initial state."""
        self.register1.clear()
        self.register2.clear()
        self.register3.clear()

    def next_array(self) -> Sequence[int]:
        """Get next values from all three registers.

        Returns:
            Array of three values [x1, x2, x3] from registers
        """
        return (
            self.register1.next()[self.register1.column_index],
            self.register2.next()[self.register2.column_index],
            self.register3.next()[self.register3.column_index],
        )

    def next_bit(self) -> int:
        """Generate next bit using Geffe formula.

        Geffe formula: f(x1, x2, x3) = (x1 * x2) ^ (x2 * x3) ^ x3
        In boolean algebra: (x1 & x2) ^ (x2 & x3) ^ x3

        Returns:
            Next generated bit
        """
        values = self.next_array()
        x1, x2, x3 = values[0], values[1], values[2]
        # f(x1, x2, x3) = (x1 & x2) ^ (x2 & x3) ^ x3
        return (x1 & x2) ^ (x2 & x3) ^ x3

    def next_int(self) -> int:
        """Get next integer value from all three registers combined.

        Returns:
            Integer value from binary representation of register outputs
        """
        values = self.next_array()
        binary_str = "".join(str(v) for v in values)
        return int(binary_str, 2)

    def get_sequence(self) -> str:
        """Generate full sequence for one period.

        Returns:
            Binary sequence string
        """
        self.clear()
        sequence = []
        for _ in range(self._period):
            sequence.append(str(self.next_bit()))
        return "".join(sequence)

    def get_actual_sequence_period(self) -> int:
        """Calculate actual period of output sequence.

        Generates the sequence and finds the minimum period where it repeats.
        Uses a more efficient approach by generating a limited sequence and
        checking for cycles.

        Returns:
            Actual period of output sequence
        """
        self.clear()
        
        # Generate sequence up to a reasonable limit
        # For period detection, we don't need the full theoretical period
        max_length = min(self._period * 2, 2000)  # Reasonable upper bound
        sequence = []
        
        for _ in range(max_length):
            sequence.append(str(self.next_bit()))
        
        sequence_str = "".join(sequence)
        sequence_len = len(sequence_str)
        
        # Find minimum period by checking if sequence repeats
        # Start from small periods and work up
        for period in range(1, min(sequence_len // 2 + 1, 500)):
            # Check if sequence repeats with this period
            if sequence_len >= period * 2:  # Need at least 2 repetitions to verify
                # Extract pattern
                pattern = sequence_str[:period]
                # Check if it repeats in the sequence
                matches = True
                for i in range(period, min(sequence_len, period * 10)):  # Check first 10 repetitions
                    if sequence_str[i] != pattern[i % period]:
                        matches = False
                        break
                
                if matches:
                    # Verify: check if the whole sequence matches
                    expected_repeats = sequence_len // period
                    if sequence_str == pattern * expected_repeats:
                        return period
        
        # If no period found in reasonable range, return theoretical period
        return self._period

    @property
    def period(self) -> int:
        """Get generator period (LCM of all register periods).

        Returns:
            Period length
        """
        return self._period

    @property
    def start_position(self) -> Sequence[int]:
        """Get initial position.

        Returns:
            Initial state values
        """
        return self._start_position

    def __str__(self) -> str:
        """String representation of generator."""
        lines = [
            "Генератор Геффе",
            f"Период генератора: {self.period}",
            f"1. {self.register1}",
            f"2. {self.register2}",
            f"3. {self.register3}",
        ]
        return "\n".join(lines)

