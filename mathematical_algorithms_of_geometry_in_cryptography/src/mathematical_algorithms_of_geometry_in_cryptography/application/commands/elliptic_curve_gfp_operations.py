import logging
from dataclasses import dataclass
from typing import Final, final

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.entities.elliptic_curve_gfp import (
    EllipticCurveGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.services.elliptic_curve_gfp_service import (
    EllipticCurveGFpService,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.curve_parameters_gfp import (
    CurveParametersGFp,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.field_parameter import (
    FieldParameter,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve_gfp.values.gfp_point import (
    GFpPoint,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateEllipticCurveGFpCommand:
    """Команда для генерации эллиптической кривой над GF(p)."""

    a: int
    b: int
    p: int


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPointsCommand:
    """Команда для сложения двух точек на эллиптической кривой."""

    curve: EllipticCurveGFp
    p_x: int
    p_y: int
    q_x: int
    q_y: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DoublePointCommand:
    """Команда для удвоения точки на эллиптической кривой."""

    curve: EllipticCurveGFp
    p_x: int
    p_y: int


@dataclass(frozen=True, slots=True, kw_only=True)
class MultiplyPointCommand:
    """Команда для скалярного умножения точки на эллиптической кривой."""

    curve: EllipticCurveGFp
    p_x: int
    p_y: int
    multiplier: int


@final
class GenerateEllipticCurveGFpCommandHandler:
    """Обработчик команды генерации эллиптической кривой над GF(p)."""

    def __init__(self, elliptic_curve_gfp_service: EllipticCurveGFpService) -> None:
        """
        Инициализировать обработчик сервисом эллиптических кривых над GF(p).

        :param elliptic_curve_gfp_service: сервис для работы с эллиптическими кривыми над GF(p)
        """
        self._elliptic_curve_gfp_service: Final[EllipticCurveGFpService] = (
            elliptic_curve_gfp_service
        )

    def __call__(
        self,
        command: GenerateEllipticCurveGFpCommand,
    ) -> EllipticCurveGFp:
        """
        Обработать команду генерации эллиптической кривой.

        :param command: команда с параметрами кривой
        :return: сгенерированная эллиптическая кривая
        """
        logger.info(
            "Начинается генерация эллиптической кривой над GF(p). "
            "Параметры: a=%s, b=%s, p=%s",
            command.a,
            command.b,
            command.p,
        )

        # Создаем value objects
        field_parameter = FieldParameter(value=command.p)
        parameters = CurveParametersGFp(a=command.a, b=command.b, p=field_parameter)

        logger.info("Созданы value objects: parameters=%s", parameters)

        # Генерируем кривую
        curve: EllipticCurveGFp = self._elliptic_curve_gfp_service.generate_curve(
            parameters=parameters,
        )

        logger.info("Эллиптическая кривая сгенерирована. ID: %s, Порядок: %s", curve.id, curve.order)

        return curve


@final
class AddPointsCommandHandler:
    """Обработчик команды сложения точек."""

    def __init__(self, elliptic_curve_gfp_service: EllipticCurveGFpService) -> None:
        """
        Инициализировать обработчик сервисом эллиптических кривых над GF(p).

        :param elliptic_curve_gfp_service: сервис для работы с эллиптическими кривыми над GF(p)
        """
        self._elliptic_curve_gfp_service: Final[EllipticCurveGFpService] = (
            elliptic_curve_gfp_service
        )

    def __call__(
        self,
        command: AddPointsCommand,
    ) -> GFpPoint:
        """
        Обработать команду сложения точек.

        :param command: команда с точками для сложения
        :return: результат сложения P + Q
        """
        logger.info(
            "Начинается сложение точек. P=(%s, %s), Q=(%s, %s)",
            command.p_x,
            command.p_y,
            command.q_x,
            command.q_y,
        )

        p = GFpPoint(x=command.p_x, y=command.p_y)
        q = GFpPoint(x=command.q_x, y=command.q_y)

        result = self._elliptic_curve_gfp_service.add_points(
            curve=command.curve,
            p=p,
            q=q,
        )

        logger.info("Результат сложения: %s", result)

        return result


@final
class DoublePointCommandHandler:
    """Обработчик команды удвоения точки."""

    def __init__(self, elliptic_curve_gfp_service: EllipticCurveGFpService) -> None:
        """
        Инициализировать обработчик сервисом эллиптических кривых над GF(p).

        :param elliptic_curve_gfp_service: сервис для работы с эллиптическими кривыми над GF(p)
        """
        self._elliptic_curve_gfp_service: Final[EllipticCurveGFpService] = (
            elliptic_curve_gfp_service
        )

    def __call__(
        self,
        command: DoublePointCommand,
    ) -> GFpPoint:
        """
        Обработать команду удвоения точки.

        :param command: команда с точкой для удвоения
        :return: результат удвоения 2P
        """
        logger.info("Начинается удвоение точки. P=(%s, %s)", command.p_x, command.p_y)

        p = GFpPoint(x=command.p_x, y=command.p_y)

        result = self._elliptic_curve_gfp_service.double_point(
            curve=command.curve,
            p=p,
        )

        logger.info("Результат удвоения: %s", result)

        return result


@final
class MultiplyPointCommandHandler:
    """Обработчик команды скалярного умножения точки."""

    def __init__(self, elliptic_curve_gfp_service: EllipticCurveGFpService) -> None:
        """
        Инициализировать обработчик сервисом эллиптических кривых над GF(p).

        :param elliptic_curve_gfp_service: сервис для работы с эллиптическими кривыми над GF(p)
        """
        self._elliptic_curve_gfp_service: Final[EllipticCurveGFpService] = (
            elliptic_curve_gfp_service
        )

    def __call__(
        self,
        command: MultiplyPointCommand,
    ) -> GFpPoint:
        """
        Обработать команду скалярного умножения точки.

        :param command: команда с точкой и множителем
        :return: результат скалярного умножения mP
        """
        logger.info(
            "Начинается скалярное умножение точки. P=(%s, %s), m=%s",
            command.p_x,
            command.p_y,
            command.multiplier,
        )

        p = GFpPoint(x=command.p_x, y=command.p_y)

        result = self._elliptic_curve_gfp_service.multiply_point(
            curve=command.curve,
            p=p,
            m=command.multiplier,
        )

        logger.info("Результат скалярного умножения: %sP = %s", command.multiplier, result)

        return result


