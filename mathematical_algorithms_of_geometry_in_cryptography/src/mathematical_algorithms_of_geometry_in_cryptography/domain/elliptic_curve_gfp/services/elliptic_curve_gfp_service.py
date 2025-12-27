import logging
from typing import Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.services.base import DomainService
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.entities.elliptic_curve_gfp import (
    EllipticCurveGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.errors.elliptic_curve_gfp_errors import (
    CurveGenerationError,
    PointNotOnCurveError,
    PointOperationError,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.ports.elliptic_curve_gfp_id_generator import (
    EllipticCurveGFpIDGenerator,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.curve_parameters_gfp import (
    CurveParametersGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.gfp_point import (
    GFpPoint,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class EllipticCurveGFpService(DomainService):
    """
    Domain service for working with elliptic curves over GF(p).
    
    This service encapsulates the business logic for:
    - Finding all points on the curve
    - Adding points
    - Doubling points
    - Modular arithmetic operations
    """

    def __init__(self, elliptic_curve_gfp_id_generator: EllipticCurveGFpIDGenerator) -> None:
        super().__init__()
        self._elliptic_curve_gfp_id_generator: Final[EllipticCurveGFpIDGenerator] = (
            elliptic_curve_gfp_id_generator
        )

    @staticmethod
    def _pow_mod(base: int, exp: int, mod: int) -> int:
        """
        Compute base^exp mod mod using fast exponentiation.
        
        Args:
            base: Base number
            exp: Exponent
            mod: Modulus
            
        Returns:
            base^exp mod mod
        """
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result

    @staticmethod
    def _mod_inverse(a: int, p: int) -> int:
        """
        Compute modular inverse of a modulo p using Fermat's little theorem.
        
        Args:
            a: Number to invert
            p: Prime modulus
            
        Returns:
            a^(-1) mod p
        """
        return EllipticCurveGFpService._pow_mod(a, p - 2, p)

    def _find_all_points(self, parameters: CurveParametersGFp) -> list[GFpPoint]:
        """
        Find all points on the elliptic curve y² = x³ + ax + b over GF(p).
        
        Args:
            parameters: Curve parameters
            
        Returns:
            List of all points on the curve (including infinity point)
        """
        a = parameters.a
        b = parameters.b
        p = int(parameters.p)
        points: list[GFpPoint] = []

        logger.info("Поиск всех точек кривой y² = x³ + %sx + %s над GF(%s)", a, b, p)

        for x in range(p):
            # Calculate right-hand side: x³ + ax + b mod p
            rhs = ((x ** 3) + a * x + b) % p
            logger.debug("x = %s, x³ + ax + b = %s mod %s", x, rhs, p)

            # Check all possible y values
            for y in range(p):
                y_squared = (y ** 2) % p
                logger.debug("  y = %s, y² = %s mod %s", y, y_squared, p)

                if y_squared == rhs:
                    point = GFpPoint(x=x, y=y)
                    points.append(point)
                    logger.debug("  Найдена точка: %s", point)

        # Add infinity point
        infinity_point = GFpPoint.infinity()
        points.append(infinity_point)
        logger.info("Найдено %s точек на кривой (включая точку бесконечности)", len(points))

        return points

    def generate_curve(self, parameters: CurveParametersGFp) -> EllipticCurveGFp:
        """
        Generate an elliptic curve over GF(p) with given parameters.
        
        Args:
            parameters: Curve parameters (a, b, p)
            
        Returns:
            EllipticCurveGFp aggregate with all points
            
        Raises:
            CurveGenerationError: If curve generation fails
        """
        try:
            logger.info(
                "Начинается генерация эллиптической кривой y² = x³ + %sx + %s над GF(%s)",
                parameters.a,
                parameters.b,
                parameters.p,
            )

            # Find all points
            points = self._find_all_points(parameters)

            # Create aggregate
            curve = EllipticCurveGFp(
                id=self._elliptic_curve_gfp_id_generator(),
                parameters=parameters,
                points=points,
            )

            logger.info(
                "Эллиптическая кривая успешно сгенерирована. "
                "Порядок кривой: %s",
                curve.order,
            )

            return curve

        except Exception as e:
            msg = f"Failed to generate elliptic curve: {e}"
            logger.error(msg)
            raise CurveGenerationError(msg) from e

    def add_points(
        self,
        curve: EllipticCurveGFp,
        p: GFpPoint,
        q: GFpPoint,
    ) -> GFpPoint:
        """
        Add two points P and Q on the elliptic curve.
        
        Args:
            curve: The elliptic curve
            p: First point
            q: Second point
            
        Returns:
            Result of P + Q
            
        Raises:
            PointNotOnCurveError: If points don't belong to the curve
            PointOperationError: If point addition fails
        """
        try:
            p_value = int(curve.parameters.p)
            a = curve.parameters.a

            logger.info("Сложение точек: %s + %s", p, q)

            # Check if points are on the curve
            if not curve.contains_point(p):
                msg = f"Point {p} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            if not curve.contains_point(q):
                msg = f"Point {q} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            # Handle infinity point
            if p.is_infinity:
                logger.info("P - точка бесконечности, результат: %s", q)
                return q

            if q.is_infinity:
                logger.info("Q - точка бесконечности, результат: %s", p)
                return p

            # Check if P + Q = O (points are inverses)
            if p.x == q.x and (p.y + q.y) % p_value == 0:
                logger.info("Точки являются обратными, результат: O")
                return GFpPoint.infinity()

            # Calculate lambda
            if p == q:
                # Point doubling: λ = (3x² + a) / (2y)
                numerator = (3 * p.x * p.x + a) % p_value
                denominator = self._mod_inverse(2 * p.y, p_value)
                logger.info("Удвоение точки: числитель = %s, знаменатель = %s", numerator, denominator)
            else:
                # Point addition: λ = (y₂ - y₁) / (x₂ - x₁)
                numerator = (q.y - p.y + p_value) % p_value
                denominator = self._mod_inverse((q.x - p.x + p_value) % p_value, p_value)
                logger.info("Сложение точек: числитель = %s, знаменатель = %s", numerator, denominator)

            lambda_val = (numerator * denominator) % p_value
            logger.info("λ = %s", lambda_val)

            # Calculate result point
            xr = (lambda_val * lambda_val - p.x - q.x) % p_value
            yr = (lambda_val * (p.x - xr) - p.y) % p_value

            result = GFpPoint(x=(xr + p_value) % p_value, y=(yr + p_value) % p_value)
            logger.info("Результат: %s", result)

            return result

        except (PointNotOnCurveError, PointOperationError):
            raise
        except Exception as e:
            msg = f"Failed to add points: {e}"
            logger.error(msg)
            raise PointOperationError(msg) from e

    def double_point(
        self,
        curve: EllipticCurveGFp,
        p: GFpPoint,
    ) -> GFpPoint:
        """
        Double a point P on the elliptic curve (compute 2P).
        
        Args:
            curve: The elliptic curve
            p: Point to double
            
        Returns:
            Result of 2P
            
        Raises:
            PointNotOnCurveError: If point doesn't belong to the curve
            PointOperationError: If point doubling fails
        """
        logger.info("Удвоение точки: 2 * %s", p)
        return self.add_points(curve, p, p)

