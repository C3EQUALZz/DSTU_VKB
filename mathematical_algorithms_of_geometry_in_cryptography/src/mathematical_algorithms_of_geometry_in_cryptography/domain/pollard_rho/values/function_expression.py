from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.values.base import BaseValueObject
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.errors.pollard_rho_errors import (
    InvalidFunctionError,
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class FunctionExpression(BaseValueObject):
    """
    Value object representing a mathematical function expression f(x).
    
    The expression should be a valid mathematical expression with variable 'x'.
    Example: "x^2 + 1", "x^2 - 1", etc.
    """

    expression: str

    def _validate(self) -> None:
        """Validate that the function expression is not empty."""
        if not self.expression or not self.expression.strip():
            msg = "Function expression cannot be empty"
            raise InvalidFunctionError(msg)

        # Basic check: expression should contain 'x' as variable
        if "x" not in self.expression.lower():
            msg = "Function expression must contain variable 'x'"
            raise InvalidFunctionError(msg)

    def __str__(self) -> str:
        return self.expression


