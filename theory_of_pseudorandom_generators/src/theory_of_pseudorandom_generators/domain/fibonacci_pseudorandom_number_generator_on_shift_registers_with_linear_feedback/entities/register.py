"""Register entity for Fibonacci generator."""

from collections.abc import Sequence
from dataclasses import dataclass, field

from theory_of_pseudorandom_generators.domain.common.entities.base_aggregate import (
    BaseAggregateRoot,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.errors import (
    ColumnIndexOutOfBoundsError,
    InvalidPolynomialAfterNormalizationError,
    WrongPolynomialDegreeError,
)
from theory_of_pseudorandom_generators.domain.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback.values.register_id import (
    RegisterID,
)


def normalize_polynomial(coefficients: Sequence[int]) -> Sequence[int]:
    """Normalize polynomial coefficients to GF(2).

    Args:
        coefficients: Polynomial coefficients

    Returns:
        Normalized coefficients in GF(2)
    """
    # Remove trailing zeros
    coeffs = list(coefficients)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()

    # Bring to GF(2) - all coefficients mod 2
    coeffs = [c % 2 for c in coeffs]

    # Ensure at least one coefficient
    if not coeffs:
        coeffs = [0]

    return tuple(coeffs)


def get_polynomial_degree(coefficients: Sequence[int]) -> int:
    """Get polynomial degree.

    Args:
        coefficients: Polynomial coefficients

    Returns:
        Polynomial degree
    """
    normalized = normalize_polynomial(coefficients)
    return len(normalized) - 1


def multiply_matrices_mod2(matrix_a: list[list[int]], matrix_b: list[list[int]]) -> list[list[int]]:
    """Multiply two matrices modulo 2.

    Args:
        matrix_a: First matrix
        matrix_b: Second matrix

    Returns:
        Result of multiplication modulo 2
    """
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])

    if cols_a != rows_b:
        msg = "Matrix dimensions don't match for multiplication"
        raise ValueError(msg)

    result = [[0] * cols_b for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] = (result[i][j] + matrix_a[i][k] * matrix_b[k][j]) % 2

    return result


@dataclass(eq=False, kw_only=True)
class Register(BaseAggregateRoot[RegisterID]):
    """Fibonacci generator register with linear feedback shift."""

    polynomial_coefficients: Sequence[int]
    start_position: Sequence[int]
    shift: int
    column_index: int = 0

    _register: list[list[int]] = field(init=False, repr=False)
    _transition_matrix_t: list[list[int]] = field(init=False, repr=False)
    _transition_matrix_v: list[list[int]] = field(init=False, repr=False)
    _max_period: int = field(init=False, repr=False)
    _normalized_polynomial: Sequence[int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize register after creation."""
        super().__post_init__()

        # Normalize polynomial
        self._normalized_polynomial = normalize_polynomial(self.polynomial_coefficients)
        degree = get_polynomial_degree(self._normalized_polynomial)

        # Validate column index
        if self.column_index < 0 or self.column_index >= len(self.start_position):
            msg = "Индекс выходит за пределы границ регистра"
            raise ColumnIndexOutOfBoundsError(msg)

        # Validate polynomial degree matches start position length
        if degree != len(self.start_position):
            msg = "Степень многочлена и длина начальной позиции не равны"
            raise WrongPolynomialDegreeError(msg)

        # Validate polynomial after normalization
        if degree < 2:
            msg = "Полином после нормализации не подходит"
            raise InvalidPolynomialAfterNormalizationError(msg)

        # Initialize matrices
        self._transition_matrix_t = self._build_transition_matrix_t()
        self._transition_matrix_v = self._build_transition_matrix_v()
        self._max_period = 2**degree - 1

        # Initialize register state
        self._register = [[0] * degree, [0] * degree]
        self.clear()

    def clear(self) -> None:
        """Reset register to initial state."""
        self._register[0] = list(self.start_position)
        self._register[1] = [0] * len(self.start_position)

    def _build_transition_matrix_t(self) -> list[list[int]]:
        """Build transition matrix T from polynomial.

        Returns:
            Transition matrix T
        """
        degree = len(self.start_position)
        matrix = [[0] * degree for _ in range(degree)]

        # First row: polynomial coefficients from x^1 to x^degree
        # In Java: T[0] = Arrays.copyOfRange(polynomial.getCoefficients(), 1, degree + 1)
        coeffs = self._normalized_polynomial
        # coeffs[0] is x^0, coeffs[1] is x^1, ..., coeffs[degree] is x^degree
        for i in range(degree):
            if i + 1 < len(coeffs):
                matrix[0][i] = coeffs[i + 1] % 2
            else:
                matrix[0][i] = 0

        # Identity submatrix: T[i][i-1] = 1 for i = 1..degree-1
        for i in range(1, degree):
            matrix[i][i - 1] = 1

        return matrix

    def _build_transition_matrix_v(self) -> list[list[int]]:
        """Build transition matrix V = T^k.

        Returns:
            Transition matrix V
        """
        if self.shift <= 0:
            msg = "Shift must be positive"
            raise ValueError(msg)

        # In Java: V = T; then for i=1 to shift-1: V = multiply(V, T)
        # So if shift=1, V=T. If shift=2, V=T*T, etc.
        v = [row[:] for row in self._transition_matrix_t]  # Copy T
        # Multiply T by itself (shift - 1) times
        for _ in range(1, self.shift):
            v = multiply_matrices_mod2(v, self._transition_matrix_t)

        return v

    def next(self, count: int | None = None) -> Sequence[int]:
        """Get next register state.

        Args:
            count: Number of cells to return (default: all)

        Returns:
            Next state values
        """
        if count is None:
            count = len(self.start_position)

        length = len(self._register[0])
        out = tuple(self._register[0][length - count : length])
        self._step()
        return out

    def _step(self) -> None:
        """Perform one step of register shift."""
        v = self._transition_matrix_v
        register = self._register

        # Calculate new state: register[1] = V * register[0]
        for i in range(len(v)):
            register[1][i] = 0
            for j in range(len(v[0])):
                if v[i][j] == 1:
                    register[1][i] = (register[1][i] + register[0][j]) % 2

        # Move new state to current state
        register[0] = register[1][:]
        register[1] = [0] * len(register[0])

    def get_period(self) -> int:
        """Calculate period by counting cycles.

        Returns:
            Period length
        """
        self.clear()
        self.next()
        period = 1

        start_state = list(self.start_position)
        while list(self._register[0]) != start_state:
            self.next()
            period += 1

        return period

    @property
    def max_period(self) -> int:
        """Get maximum possible period (2^n - 1).

        Returns:
            Maximum period
        """
        return self._max_period

    @property
    def transition_matrix_t(self) -> list[list[int]]:
        """Get transition matrix T.

        Returns:
            Matrix T
        """
        return [row[:] for row in self._transition_matrix_t]

    @property
    def transition_matrix_v(self) -> list[list[int]]:
        """Get transition matrix V.

        Returns:
            Matrix V
        """
        return [row[:] for row in self._transition_matrix_v]

    def __str__(self) -> str:
        """String representation of register."""
        lines = [
            "Генератор Фибоначчи:",
            f"Примитивный многочлен: {self._normalized_polynomial}",
            f"Количество ячеек: {len(self.start_position)}",
            "Матрица состояний T:",
            "\n".join(str(row) for row in self._transition_matrix_t),
            "Матрица переходов V:",
            "\n".join(str(row) for row in self._transition_matrix_v),
            f"Значение сдвига k: {self.shift}",
            f"Начальное состояние: {list(self.start_position)}",
            f"Период: {self.max_period}",
        ]
        return "\n".join(lines)



