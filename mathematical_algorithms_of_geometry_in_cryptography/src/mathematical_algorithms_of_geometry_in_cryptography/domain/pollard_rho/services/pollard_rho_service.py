import logging
import math
from typing import Final, Optional

from sympy import Symbol, sympify, N

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.services.base import DomainService
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.entities.pollard_rho_test import (
    PollardRhoTest,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.errors.pollard_rho_errors import (
    DivisorNotFoundError,
    FunctionEvaluationError,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.ports.pollard_rho_id_generator import (
    PollardRhoIDGenerator,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.function_expression import (
    FunctionExpression,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.initial_value import (
    InitialValue,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.number import (
    Number,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.pollard_rho.values.step_result import (
    StepResult,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PollardRhoService(DomainService):
    """
    Domain service for performing Pollard's Rho algorithm to find a non-trivial divisor.
    
    This service encapsulates the business logic for:
    - Evaluating function expressions
    - Computing GCD
    - Performing Pollard's Rho algorithm
    """

    def __init__(self, pollard_rho_id_generator: PollardRhoIDGenerator) -> None:
        super().__init__()
        self._pollard_rho_id_generator: Final[PollardRhoIDGenerator] = pollard_rho_id_generator

    def _evaluate_function(
        self,
        expression: FunctionExpression,
        x: int,
        mod: int,
    ) -> int:
        """
        Evaluate function f(x) mod n.
        
        Args:
            expression: The function expression
            x: The value to substitute
            mod: The modulus
            
        Returns:
            f(x) mod n
            
        Raises:
            FunctionEvaluationError: If function evaluation fails
        """
        try:
            # Parse the expression
            x_symbol = Symbol("x")
            expr = sympify(expression.expression)
            
            # Substitute x and evaluate
            result = expr.subs(x_symbol, x)
            result_float = float(N(result))
            result_int = int(result_float)
            
            # Return result mod n
            return result_int % mod
        except Exception as e:
            msg = f"Failed to evaluate function '{expression.expression}' with x={x}: {e}"
            logger.error(msg)
            raise FunctionEvaluationError(msg) from e

    def find_divisor(
        self,
        n: Number,
        c: InitialValue,
        function: FunctionExpression,
    ) -> PollardRhoTest:
        """
        Find a non-trivial divisor of n using Pollard's Rho algorithm.
        
        Args:
            n: The number to factor
            c: The initial value
            function: The function expression f(x)
            
        Returns:
            PollardRhoTest aggregate containing all step results and the divisor (if found)
            
        Raises:
            DivisorNotFoundError: If d == n (divisor not found)
        """
        n_value = int(n)
        c_value = int(c)

        # Check if n is even
        if n_value % 2 == 0:
            logger.info("Число %s четное, делитель = 2", n_value)
            test = PollardRhoTest(
                id=self._pollard_rho_id_generator(),
                number=n,
                initial_value=c,
                function_expression=function,
            )
            test.divisor = 2
            test.is_complete = True
            return test

        # Initialize
        a = c_value
        b = c_value
        d = 1
        step_count = 0

        test = PollardRhoTest(
            id=self._pollard_rho_id_generator(),
            number=n,
            initial_value=c,
            function_expression=function,
        )

        logger.info(
            "Начинается алгоритм Полларда для числа: %s, начальное значение: %s, функция: %s",
            n_value,
            c_value,
            function.expression,
        )

        # Main loop
        while d == 1:
            step_count += 1
            logger.info("Шаг %s", step_count)

            # Compute a = f(a) mod n
            a = self._evaluate_function(function, a, n_value)
            logger.info("a = %s", a)

            # Compute b = f(f(b)) mod n
            b_temp = self._evaluate_function(function, b, n_value)
            b = self._evaluate_function(function, b_temp, n_value)
            logger.info("b = %s", b)

            # Compute d = gcd(a - b, n)
            d = math.gcd(abs(a - b), n_value)
            logger.info("d = %s", d)
            logger.info("")

            # Create step result
            step = StepResult(
                step_number=step_count,
                a=a,
                b=b,
                d=d,
            )
            test.add_step(step)

            # Check if d == n (divisor not found)
            if d == n_value:
                logger.info("Делитель не найден (d == n)")
                test.mark_complete_no_divisor()
                raise DivisorNotFoundError(
                    f"Divisor not found: d == n ({d} == {n_value})",
                )

        # Found a divisor
        logger.info("Найден нетривиальный делитель: %s", test.divisor)
        return test


