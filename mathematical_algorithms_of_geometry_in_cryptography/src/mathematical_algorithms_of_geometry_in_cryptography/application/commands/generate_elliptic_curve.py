import logging
from dataclasses import dataclass
from typing import Final, final

from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.entities.elliptic_curve import (
    EllipticCurve,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.services.elliptic_curve_service import (
    EllipticCurveService,
)
from mathematical_algorithms_of_geometry_in_cryptography.domain.elliptic_curve.values.curve_parameters import (
    CurveParameters,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateEllipticCurveCommand:
    """Команда для генерации эллиптической кривой."""

    a: float
    b: float
    x_min: float = -2.0
    x_max: float = 2.0
    step: float = 0.00001


@final
class GenerateEllipticCurveCommandHandler:
    """Обработчик команды генерации эллиптической кривой."""

    def __init__(self, elliptic_curve_service: EllipticCurveService) -> None:
        """
        Инициализировать обработчик сервисом эллиптических кривых.

        :param elliptic_curve_service: сервис для работы с эллиптическими кривыми
        """
        self._elliptic_curve_service: Final[EllipticCurveService] = elliptic_curve_service

    def __call__(
        self,
        command: GenerateEllipticCurveCommand,
    ) -> EllipticCurve:
        """
        Обработать команду генерации эллиптической кривой.

        :param command: команда с параметрами кривой
        :return: сгенерированная эллиптическая кривая
        """
        logger.info(
            "Начинается генерация эллиптической кривой. "
            "Параметры: a=%s, b=%s, x_min=%s, x_max=%s, step=%s",
            command.a,
            command.b,
            command.x_min,
            command.x_max,
            command.step,
        )

        # Создаем value object
        parameters = CurveParameters(a=command.a, b=command.b)
        logger.info("Создан объект CurveParameters: %s", parameters)

        # Генерируем кривую
        curve: EllipticCurve = self._elliptic_curve_service.generate_curve(
            parameters=parameters,
            x_min=command.x_min,
            x_max=command.x_max,
            step=command.step,
        )

        logger.info("Эллиптическая кривая сгенерирована. ID: %s", curve.id)
        logger.info(
            "Статус сингулярности: %s, Дискриминант: %s",
            curve.singularity_status.value,
            curve.discriminant,
        )

        upper_valid, lower_valid = curve.get_valid_points()
        logger.info(
            "Количество точек: верхняя ветвь=%s, нижняя ветвь=%s",
            len(upper_valid),
            len(lower_valid),
        )

        return curve

