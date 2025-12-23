import logging
import time
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, final

from theory_of_pseudorandom_generators.application.views.polynomial_congruent_generator_view import (
    ConditionCheckResult,
    PolynomialCongruentGeneratorView,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.entities.polynomial_congruent_generator import (
    PolynomialCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.polynomial_congruent_pseudorandom_number_generator.services.polynomial_congruent_generator_service import (
    PolynomialCongruentGeneratorService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class PolynomialCongruentPseudorandomNumberGeneratorCommand:
    a1: int
    a2: int
    b: int
    m: int
    x0: int
    size: int


@final
class PolynomialCongruentPseudorandomNumberGeneratorCommandHandler:
    def __init__(
            self,
            polynomial_congruent_gen: PolynomialCongruentGeneratorService,
    ) -> None:
        self._polynomial_congruent_service: Final[PolynomialCongruentGeneratorService] = polynomial_congruent_gen

    def __call__(self, data: PolynomialCongruentPseudorandomNumberGeneratorCommand) -> PolynomialCongruentGeneratorView:
        logger.info(
            "Начинается генерация псевдослучайных чисел с помощью полиномиального конгруэнтного генератора."
            "a1 - %s, a2 - %s b - %s, m - %s, x0 - %s, size - %s",
            data.a1,
            data.a2,
            data.b,
            data.m,
            data.x0,
            data.size,
        )

        polynomial_generator: PolynomialCongruentGenerator = self._polynomial_congruent_service.create(
            a1=data.a1,
            a2=data.a2,
            b=data.b,
            x=data.x0,
            m=data.m
        )

        logger.info(
            "Создание генератора успешно! Объект - %s",
            polynomial_generator
        )

        logger.info("Начинаю генерировать последовательность")

        start_time: float = time.perf_counter()

        sequence: Iterable[int] = list(self._polynomial_congruent_service.get_random_sequence(
            generator=polynomial_generator,
            count=data.size,
        ))

        binary_sequence: Generator[str, Any, None] = (bin(x)[2:] for x in sequence)
        string_binary_sequence: str = ", ".join(binary_sequence)

        logger.info(string_binary_sequence)

        end_time: float = (time.perf_counter() - start_time) * 1000

        logger.info("Продолжительность генерации %s мс", end_time)

        # Проверка условий максимального периода с детальной информацией
        is_max_period, conditions_results = self._polynomial_congruent_service.check_max_period_conditions_detailed(
            polynomial_generator
        )
        
        if is_max_period:
            logger.info("Условие максимального периода выполнено.")
        else:
            logger.info("Условие максимального периода не выполнено.")

        start_time = time.perf_counter()

        period = self._polynomial_congruent_service.get_period(polynomial_generator)
        start_period_index = self._polynomial_congruent_service.get_start_period_index(polynomial_generator)

        end_time: float = (time.perf_counter() - start_time) * 1000

        logger.info("Период последовательности: %s", period)
        logger.info("Начало периода: %s", start_period_index)
        logger.info("Время поиска периода: %s мс", end_time)

        path_to_save: Path = Path(__file__).parent.parent.parent.parent.parent / "polynomial_congruent.txt"

        with open(path_to_save, "w", encoding="utf-8") as f:
            f.write(" ".join(map(str, sequence)))

        logger.info("Файл с параметрами генератора: %s", path_to_save)

        # Создание View с результатами проверки условий
        condition_results = tuple(
            ConditionCheckResult(
                condition_number=cond[0],
                description=cond[1],
                is_fulfilled=cond[2],
                details=cond[3],
            )
            for cond in conditions_results
        )

        return PolynomialCongruentGeneratorView(
            m=data.m,
            a1=data.a1,
            a2=data.a2,
            b=data.b,
            x0=data.x0,
            conditions=condition_results,
            is_max_period=is_max_period,
            period=period,
            start_period_index=start_period_index,
        )


