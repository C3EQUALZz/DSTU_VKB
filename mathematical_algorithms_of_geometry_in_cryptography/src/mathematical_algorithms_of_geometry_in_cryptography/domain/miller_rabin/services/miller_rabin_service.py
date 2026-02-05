import logging
import math
import random
from typing import Optional, Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.services.base import DomainService
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.entities.miller_rabin_test import (
    MillerRabinTest,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.ports.miller_rabin_id_generator import \
    MillerRabinIDGenerator
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.number import (
    Number,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.test_parameters import (
    TestParameters,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.miller_rabin.values.test_result import (
    PrimalityStatus,
    TestResult,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class MillerRabinService(DomainService):
    """
    Domain service for performing Miller-Rabin primality tests.
    
    This service encapsulates the business logic for:
    - Computing GCD
    - Decomposing n-1 into 2^s * t
    - Performing individual test iterations
    - Running complete test suites
    """

    def __init__(self, miller_id_generator: MillerRabinIDGenerator) -> None:
        super().__init__()
        self._miller_id_generator: Final[MillerRabinIDGenerator] = miller_id_generator

    @staticmethod
    def _decompose(n: int) -> tuple[int, int]:
        """
        Decompose n-1 into the form 2^s * t, where t is odd.
        
        Args:
            n: The number to decompose (n-1 will be decomposed)
            
        Returns:
            A tuple (s, t) where n-1 = 2^s * t and t is odd
        """
        n_minus_one = n - 1
        s = 0
        t = n_minus_one

        while t % 2 == 0:
            t //= 2
            s += 1

        return s, t

    def perform_single_test(
            self,
            n: Number,
            a: int,
            iteration: int,
    ) -> TestResult:
        """
        Perform a single iteration of the Miller-Rabin test.
        
        Args:
            n: The number to test
            a: The random base for the test
            iteration: The iteration number (1-based)
            
        Returns:
            TestResult containing the test outcome and intermediate values
            
        Raises:
            TestFailedError: If the number is found to be composite
        """
        n_value = int(n)
        intermediate_values: dict[str, int | str] = {}

        # Decompose n-1 = 2^s * t
        s, t = self._decompose(n_value)
        intermediate_values["s"] = s
        intermediate_values["t"] = t
        intermediate_values["a"] = a
        logger.info(
            "Шаг 1. Разложение n-1: %s - 1 = 2^s * t, где s = %s, t = %s",
            n_value,
            s,
            t,
        )
        logger.info(
            "Шаг 2. Выбор случайного основания a в диапазоне [2, n-2]: a = %s",
            a,
        )

        # Check GCD(a, n)
        nod = math.gcd(a, n_value)
        intermediate_values["gcd"] = nod
        logger.info(
            "Шаг 3. Вычисляем НОД(a, n). Если НОД(a, n) > 1, найден нетривиальный делитель n."
        )
        logger.info("       НОД(a, n) = %s", nod)


        if nod != 1:
            logger.info(
                "Так как НОД(a, n) = %s > 1, число %s составное (обнаружен делитель).",
                nod,
                n_value,
            )

            intermediate_values["reason"] = "gcd_not_one"
            return TestResult(
                status=PrimalityStatus.COMPOSITE,
                iteration=iteration,
                parameters=TestParameters(s=s, t=t, a=a),
                intermediate_values=intermediate_values,
            )

        # Perform the test
        for k in range(s):
            logger.info(
                "Шаг 4.%s. Проводим k‑ый цикл возведения в квадрат (k = %s из 0..s-1).",
                k,
                k,
            )

            # Compute b = a^t mod n
            b = pow(a, t, n_value)
            intermediate_values[f"b_k{k}"] = b
            logger.info(
                "   4.%s.1. Вычисляем b = a^t (mod n) = %s^%s (mod %s) = %s",
                k,
                a,
                t,
                n_value,
                b,
            )


            # Check if b == 1 or b == n-1
            if b == 1 or b == n_value - 1:
                logger.info(
                    "   Так как b = %s и выполняется условие (b == 1) или (b == n-1 = %s),",
                    b,
                    n_value - 1,
                )
                logger.info(
                    "   данная итерация не нашла свидетель сложности. Число %s считается вероятно простым.",
                    n_value,
                )

                intermediate_values["reason"] = f"b_equals_one_or_n_minus_one_at_k{k}"
                return TestResult(
                    status=PrimalityStatus.PROBABLY_PRIME,
                    iteration=iteration,
                    parameters=TestParameters(s=s, t=t, a=a),
                    intermediate_values=intermediate_values,
                )

            # Square b
            b = pow(b, 2, n_value)
            intermediate_values[f"b_squared_k{k}"] = b
            logger.info(
                "   4.%s.2. Возводим b в квадрат по модулю n: b = b^2 (mod n) = %s",
                k,
                b,
            )


            # Check if b == n-1
            if b == n_value - 1:
                logger.info(
                    "   Так как b = n-1 = %s, найдено значение, при котором условие теста выполняется.",
                    n_value - 1,
                )
                logger.info(
                    "   На данной итерации свидетель сложности не найден. Число %s считается вероятно простым.",
                    n_value,
                )

                intermediate_values["reason"] = f"b_squared_equals_n_minus_one_at_k{k}"
                return TestResult(
                    status=PrimalityStatus.PROBABLY_PRIME,
                    iteration=iteration,
                    parameters=TestParameters(s=s, t=t, a=a),
                    intermediate_values=intermediate_values,
                )

        # If we reach here, the number is composite
        logger.info(
            "После выполнения всех %s шагов не найдено значение b, удовлетворяющее условиям простоты.",
            s,
        )
        logger.info("Делаем вывод: число %s составное.", n_value)

        intermediate_values["reason"] = "no_witness_found"
        return TestResult(
            status=PrimalityStatus.COMPOSITE,
            iteration=iteration,
            parameters=TestParameters(s=s, t=t, a=a),
            intermediate_values=intermediate_values,
        )

    def perform_full_test(
            self,
            n: Number,
            iterations: int = 5,
            random_seed: Optional[int] = None,
    ) -> MillerRabinTest:
        """
        Perform a full Miller-Rabin test with multiple iterations.
        
        Args:
            n: The number to test
            iterations: Number of test iterations to perform (default: 5)
            random_seed: Optional seed for random number generation
            
        Returns:
            MillerRabinTest aggregate containing all test results
            
        Raises:
            TestFailedError: If any iteration finds the number to be composite
        """
        if random_seed is not None:
            random.seed(random_seed)

        test = MillerRabinTest(
            id=self._miller_id_generator(),
            number=n
        )

        n_value = int(n)

        for i in range(iterations):
            logger.info(f"%s-ая проверка", i + 1)

            # Generate random base a: 2 <= a < n-1
            a = random.randint(2, n_value - 2)

            result = self.perform_single_test(
                n=n,
                a=a,
                iteration=i + 1,
            )

            test.add_result(result)

            # If composite, stop early
            if result.status == PrimalityStatus.COMPOSITE:
                logger.info("Тест остановлен: число %s составное", n_value)
                return test

        # All iterations passed
        test.mark_complete()

        logger.info(
            "Все %s итераций пройдены. Число %s вероятно простое",
            iterations,
            n_value
        )

        return test
