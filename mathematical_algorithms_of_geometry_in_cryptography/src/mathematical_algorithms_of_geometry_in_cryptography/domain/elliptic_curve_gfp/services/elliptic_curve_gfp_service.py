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

            # Special case: order of infinity point is 1
            if p.is_infinity:
                logger.info("Точка бесконечности имеет порядок 1")
                return 1

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
            # Handle infinity point case
            if q.is_infinity:
                q_inverse = GFpPoint.infinity()
            else:
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

    def reverse_point(self, curve: EllipticCurveGFp, point: GFpPoint) -> GFpPoint:
        """
        Get the inverse point -P = (x, -y mod p).
        
        Args:
            curve: The elliptic curve
            point: Point to reverse
            
        Returns:
            Inverse point -P
        """
        if point.is_infinity:
            return GFpPoint.infinity()
        p_value = int(curve.parameters.p)
        return GFpPoint(x=point.x, y=(-point.y + p_value) % p_value)

    def find_all_orders(self, curve: EllipticCurveGFp) -> dict[GFpPoint, int]:
        """
        Find orders of all points on the elliptic curve.
        
        Args:
            curve: The elliptic curve
            
        Returns:
            Dictionary mapping points to their orders
        """
        logger.info("Начинается поиск порядков всех точек кривой")
        orders: dict[GFpPoint, int] = {}

        for point in curve.points:
            try:
                order = self.order_of_point(curve, point)
                orders[point] = order
                logger.debug("Точка %s: порядок = %s", point, order)
            except Exception as e:
                logger.warning("Не удалось найти порядок точки %s: %s", point, e)
                # Skip points that fail order calculation
                continue

        logger.info("Найдены порядки всех %s точек", len(orders))
        return orders

    def generate_sequence(
        self,
        curve: EllipticCurveGFp,
        c: int,
        x0: GFpPoint,
        p: GFpPoint,
        count: int,
        is_congruent: bool,
    ) -> tuple[list[GFpPoint], int, str]:
        """
        Generate pseudorandom sequence using congruent or inversive generator.
        
        Congruent generator: X_i = c * X_{i-1} + P
        Inversive generator: X_i = c * X_{i-1}^(-1) + P
        
        Args:
            curve: The elliptic curve
            c: Multiplier coefficient
            x0: Initial point X0
            p: Point P
            count: Number of iterations
            is_congruent: True for congruent generator, False for inversive
            
        Returns:
            Tuple of (sequence, period, binary_sequence)
        """
        try:
            p_value = int(curve.parameters.p)
            generator_type = "Конгруэнтный" if is_congruent else "Инверсивный"
            logger.info(
                "Начинается генерация последовательности (%s генератор). "
                "c=%s, X0=%s, P=%s, итераций=%s",
                generator_type,
                c,
                x0,
                p,
                count,
            )

            # Check if points are on the curve
            if not curve.contains_point(x0):
                msg = f"Point X0 {x0} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            if not curve.contains_point(p):
                msg = f"Point P {p} does not belong to the curve"
                raise PointNotOnCurveError(msg)

            # Initialize sequence
            sequence: list[GFpPoint] = [x0]
            binary_sequence = str(x0.y & 1 if not x0.is_infinity else 0)
            period = 0

            logger.info("X₀ = %s", x0)

            # Generate sequence
            for i in range(1, count):
                # Compute c * X_{i-1} or c * X_{i-1}^(-1)
                if is_congruent:
                    # Congruent: c * X_{i-1}
                    mp = self.multiply_point(curve, sequence[i - 1], c)
                    logger.info(
                        "X%s = %s * %s + %s = %s + %s",
                        self._subscript(i),
                        c,
                        sequence[i - 1],
                        p,
                        mp,
                        p,
                    )
                else:
                    # Inversive: c * X_{i-1}^(-1)
                    reversed_point = self.reverse_point(curve, sequence[i - 1])
                    mp = self.multiply_point(curve, reversed_point, c)
                    logger.info(
                        "X%s = %s * %s^(-1) + %s = %s * %s + %s = %s + %s",
                        self._subscript(i),
                        c,
                        sequence[i - 1],
                        p,
                        c,
                        reversed_point,
                        p,
                        mp,
                        p,
                    )

                # X_i = mp + P
                next_point = self.add_points(curve, mp, p)
                sequence.append(next_point)

                # Add to binary sequence (least significant bit of y)
                bit = next_point.y & 1 if not next_point.is_infinity else 0
                binary_sequence += str(bit)

                logger.info(" = %s", next_point)

                # Period detection: period is the smallest k > 0 such that X_k == X_0
                if period == 0 and next_point == x0:
                    period = i
                    logger.info("Период найден: %s (X%s = X₀)", period, self._subscript(i))

            # If period not found in initial count, continue searching
            if period == 0:
                logger.info("Период не найден в первых %s итерациях, продолжаем поиск", count)
                current = sequence[-1]
                iteration = count

                while True:
                    if is_congruent:
                        mp = self.multiply_point(curve, current, c)
                    else:
                        reversed_point = self.reverse_point(curve, current)
                        mp = self.multiply_point(curve, reversed_point, c)

                    current = self.add_points(curve, mp, p)
                    iteration += 1

                    # Period detection: period is the smallest k > 0 such that X_k == X_0
                    if current == x0:
                        period = iteration
                        logger.info("Период найден: %s (X%s = X₀)", period, self._subscript(iteration))
                        break

            logger.info("Период: %s", period)
            logger.info("Двоичная последовательность: %s", binary_sequence)

            return sequence, period, binary_sequence

        except (PointNotOnCurveError, PointOperationError):
            raise
        except Exception as e:
            msg = f"Failed to generate sequence: {e}"
            logger.error(msg)
            raise PointOperationError(msg) from e

    @staticmethod
    def _subscript(number: int) -> str:
        """
        Convert number to subscript string.
        
        Args:
            number: Number to convert
            
        Returns:
            String with subscript digits
        """
        subscript_map = {
            "0": "₀",
            "1": "₁",
            "2": "₂",
            "3": "₃",
            "4": "₄",
            "5": "₅",
            "6": "₆",
            "7": "₇",
            "8": "₈",
            "9": "₉",
        }
        return "".join(subscript_map.get(d, d) for d in str(number))

