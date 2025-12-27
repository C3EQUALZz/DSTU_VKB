import logging
from math import sqrt
from typing import Final

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.services.base import DomainService
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.entities.elliptic_curve import (
    EllipticCurve,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.errors.elliptic_curve_errors import (
    CurveGenerationError,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.ports.elliptic_curve_id_generator import (
    EllipticCurveIDGenerator,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.curve_parameters import (
    CurveParameters,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.point import (
    Point,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.singularity_status import (
    SingularityStatus,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class EllipticCurveService(DomainService):
    """
    Domain service for working with elliptic curves.
    
    This service encapsulates the business logic for:
    - Checking singularity (discriminant calculation)
    - Generating curve points
    """

    def __init__(self, elliptic_curve_id_generator: EllipticCurveIDGenerator) -> None:
        super().__init__()
        self._elliptic_curve_id_generator: Final[EllipticCurveIDGenerator] = elliptic_curve_id_generator

    @staticmethod
    def _calculate_discriminant(parameters: CurveParameters) -> float:
        """
        Calculate the discriminant Δ = 4a³ + 27b².
        
        Args:
            parameters: Curve parameters
            
        Returns:
            Discriminant value
        """
        a = parameters.a
        b = parameters.b
        discriminant = 4 * (a ** 3) + 27 * (b ** 2)
        logger.info("Дискриминант Δ = 4a³ + 27b² = 4*(%s)³ + 27*(%s)² = %s", a, b, discriminant)
        return discriminant

    @staticmethod
    def _check_singularity(discriminant: float) -> SingularityStatus:
        """
        Check if the curve is singular based on discriminant.
        
        Args:
            discriminant: The discriminant value
            
        Returns:
            SingularityStatus indicating if curve is singular or non-singular
        """
        if discriminant == 0:
            status = SingularityStatus.SINGULAR
            logger.info("Кривая сингулярная (Δ = 0)")
        else:
            status = SingularityStatus.NON_SINGULAR
            logger.info("Кривая несингулярная (Δ %s 0)", "<" if discriminant < 0 else ">")

        return status

    def _generate_curve_points(
        self,
        parameters: CurveParameters,
        x_min: float = -2.0,
        x_max: float = 2.0,
        step: float = 0.00001,
    ) -> tuple[list[Point], list[Point]]:
        """
        Generate points on the elliptic curve y² = x³ + ax + b.
        
        Args:
            parameters: Curve parameters
            x_min: Minimum x value
            x_max: Maximum x value
            step: Step size for x values
            
        Returns:
            Tuple of (upper_branch_points, lower_branch_points)
        """
        a = parameters.a
        b = parameters.b
        upper_branch: list[Point] = []
        lower_branch: list[Point] = []

        logger.info(
            "Генерация точек кривой для x от %s до %s с шагом %s",
            x_min,
            x_max,
            step,
        )

        x_values = []
        x = x_min
        while x <= x_max:
            x_values.append(x)
            x += step

        last_valid = False
        points_count = 0

        for x in x_values:
            # Calculate y² = x³ + ax + b
            y_squared = (x ** 3) + a * x + b

            if y_squared >= 0:
                # Point exists on the curve
                y = sqrt(y_squared)
                upper_branch.append(Point(x=x, y=y))
                lower_branch.append(Point(x=x, y=-y))
                last_valid = True
                points_count += 1
            elif last_valid:
                # Add NaN to break the line
                upper_branch.append(Point(x=x, y=float("nan")))
                lower_branch.append(Point(x=x, y=float("nan")))
                last_valid = False

        logger.info("Сгенерировано %s точек на кривой", points_count)
        return upper_branch, lower_branch

    def generate_curve(
        self,
        parameters: CurveParameters,
        x_min: float = -2.0,
        x_max: float = 2.0,
        step: float = 0.00001,
    ) -> EllipticCurve:
        """
        Generate an elliptic curve with given parameters.
        
        Args:
            parameters: Curve parameters (a, b)
            x_min: Minimum x value for point generation
            x_max: Maximum x value for point generation
            step: Step size for x values
            
        Returns:
            EllipticCurve aggregate with all calculated properties
            
        Raises:
            CurveGenerationError: If curve generation fails
        """
        try:
            logger.info(
                "Начинается генерация эллиптической кривой y² = x³ + %sx + %s",
                parameters.a,
                parameters.b,
            )

            # Calculate discriminant
            discriminant = self._calculate_discriminant(parameters)

            # Check singularity
            singularity_status = self._check_singularity(discriminant)

            # Generate curve points
            upper_branch, lower_branch = self._generate_curve_points(
                parameters=parameters,
                x_min=x_min,
                x_max=x_max,
                step=step,
            )

            # Create aggregate
            curve = EllipticCurve(
                id=self._elliptic_curve_id_generator(),
                parameters=parameters,
                singularity_status=singularity_status,
                discriminant=discriminant,
                upper_branch_points=upper_branch,
                lower_branch_points=lower_branch,
            )

            logger.info(
                "Эллиптическая кривая успешно сгенерирована. "
                "Статус: %s, Дискриминант: %s, Точек: %s",
                singularity_status.value,
                discriminant,
                len([p for p in upper_branch if p.is_valid]),
            )

            return curve

        except Exception as e:
            msg = f"Failed to generate elliptic curve: {e}"
            logger.error(msg)
            raise CurveGenerationError(msg) from e


