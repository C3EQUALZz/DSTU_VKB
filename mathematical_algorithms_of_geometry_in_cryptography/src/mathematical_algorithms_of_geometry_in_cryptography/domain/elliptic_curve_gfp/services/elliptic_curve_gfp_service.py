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

    def multiply_point(
        self,
        curve: EllipticCurveGFp,
        p: GFpPoint,
        m: int,
    ) -> GFpPoint:
        """
        Multiply a point P by a scalar m (compute mP) using dynamic programming.
        
        Args:
            curve: The elliptic curve
            p: Point to multiply
            m: Scalar multiplier
            
        Returns:
            Result of mP
            
        Raises:
            PointNotOnCurveError: If point doesn't belong to the curve
            PointOperationError: If point multiplication fails
        """
        try:
            if m <= 0:
                msg = f"Multiplier must be positive, got {m}"
                raise ValueError(msg)

            if m == 1:
                logger.info("m = 1, результат: %s", p)
                return p

            # Check if point is on the curve
            if not curve.contains_point(p):
                msg = f"Point {p} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            # Initialize array for dynamic programming
            point_array: list[GFpPoint] = [p] * m
            point_array[0] = p
            logger.info("P = %s", point_array[0])

            # Compute mP using dynamic programming
            for i in range(2, m + 1):
                logger.info("")
                if i % 2 == 0:
                    # Even: iP = 2 * (i/2)P
                    half_index = i // 2 - 1
                    point_array[i - 1] = self.double_point(curve, point_array[half_index])
                    half_str = "" if i // 2 == 1 else f"{i // 2}"
                    logger.info(
                        "%sP = 2 * %sP = 2 * %s = %s",
                        i,
                        half_str if half_str else "",
                        point_array[half_index],
                        point_array[i - 1],
                    )
                else:
                    # Odd: iP = (i/2)P + (i/2+1)P
                    half_index = i // 2 - 1
                    next_index = i // 2
                    point_array[i - 1] = self.add_points(
                        curve,
                        point_array[half_index],
                        point_array[next_index],
                    )
                    half_str = "" if i // 2 == 1 else f"{i // 2}"
                    logger.info(
                        "%sP = %sP + %sP = %s + %s = %s",
                        i,
                        half_str if half_str else "",
                        i // 2 + 1,
                        point_array[half_index],
                        point_array[next_index],
                        point_array[i - 1],
                    )

            logger.info("")
            logger.info("Ответ: %sP = %s", m, point_array[m - 1])
            return point_array[m - 1]

        except (PointNotOnCurveError, PointOperationError):
            raise
        except Exception as e:
            msg = f"Failed to multiply point: {e}"
            logger.error(msg)
            raise PointOperationError(msg) from e

    def order_of_point(
        self,
        curve: EllipticCurveGFp,
        p: GFpPoint,
    ) -> int:
        """
        Find the order of a point P on the elliptic curve using Baby-step Giant-step algorithm.
        
        Args:
            curve: The elliptic curve
            p: Point to find order for
            
        Returns:
            Order of point P (smallest n such that nP = O)
            
        Raises:
            PointNotOnCurveError: If point doesn't belong to the curve
            PointOperationError: If order calculation fails
        """
        try:
            import math

            p_value = int(curve.parameters.p)

            # Check if point is on the curve
            if not curve.contains_point(p):
                msg = f"Point {p} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            # Calculate N1 = p + 1 + 2*sqrt(p)
            n1 = p_value + 1 + 2 * math.sqrt(p_value)
            m = math.ceil(math.sqrt(n1))

            logger.info("N1 = %s", n1)
            logger.info("m = %s", m)

            # Build table: t -> tP for t = 1 to m
            table: dict[GFpPoint, int] = {}
            logger.info("")
            logger.info("t  Pt")

            for t in range(1, m + 1):
                pt = self.multiply_point(curve, p, t)
                table[pt] = t
                logger.info("%-3s %s", t, pt)

            logger.info("")

            # Calculate Q = mP, then -Q (inverse point)
            q = self.multiply_point(curve, p, m)
            # Inverse point: -Q = (Q.x, -Q.y mod p)
            q_inverse = GFpPoint(x=q.x, y=(-q.y + p_value) % p_value)

            logger.info("")
            logger.info("Q = %s", q_inverse)
            
            # Initialize R = O (infinity point)
            r = GFpPoint.infinity()
            logger.info("R = %s", r)

            # Baby-step Giant-step algorithm
            for i in range(m):
                logger.info("")
                logger.info("i = %s", i)

                # Check if R is in the table
                if r in table:
                    t = table[r]
                    n = m * i + t
                    logger.info(
                        "R содержится в таблице при t = %s",
                        t,
                    )
                    logger.info(
                        "n = m * i + t = %s * %s + %s = %s",
                        m,
                        i,
                        t,
                        n,
                    )
                    logger.info("")
                    logger.info("Ответ: порядок точки P равен %s", n)
                    return n

                # R = R + (-Q)
                r = self.add_points(curve, r, q_inverse)
                logger.info("R = R + Q = %s", r)

            # Should not reach here if algorithm is correct
            msg = "Failed to find point order"
            logger.error(msg)
            raise PointOperationError(msg)

        except (PointNotOnCurveError, PointOperationError):
            raise
        except Exception as e:
            msg = f"Failed to find point order: {e}"
            logger.error(msg)
            raise PointOperationError(msg) from e


