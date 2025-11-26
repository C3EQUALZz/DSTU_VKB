import logging
import time
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, final

from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.entities.linear_congruent_generator import (
    LinearCongruentGenerator,
)
from theory_of_pseudorandom_generators.domain.linear_congruent_pseudorandom_number_generator.services.linear_congruent_generator_service import (
    LinearCongruentGeneratorService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class LinearCongruentPseudorandomNumberGeneratorCommand:
    a: int
    b: int
    m: int
    x0: int
    size: int


@final
class LinearCongruentPseudorandomNumberGeneratorCommandHandler:
    def __init__(
            self,
            linear_congruent_generator_service: LinearCongruentGeneratorService,
    ) -> None:
        self._linear_congruent_service: Final[LinearCongruentGeneratorService] = linear_congruent_generator_service

    def __call__(self, data: LinearCongruentPseudorandomNumberGeneratorCommand) -> None:
        logger.info(
            "Начинается генерация псевдослучайных чисел с помощью линейного конгруэнтного генератора."
            "a - %s, b - %s, m - %s, x0 - %s, size - %s",
            data.a,
            data.b,
            data.m,
            data.x0,
            data.size,
        )

        linear_generator: LinearCongruentGenerator = self._linear_congruent_service.create(
            a=data.a,
            b=data.b,
            x=data.x0,
            m=data.m
        )

        logger.info(
            "Создание генератора успешно! Объект - %s",
            linear_generator
        )

        logger.info("Начинаю генерировать последовательность")

        start_time: float = time.perf_counter()

        sequence: Iterable[int] = list(self._linear_congruent_service.get_random_sequence(
            generator=linear_generator,
            count=data.size,
        ))

        binary_sequence: Generator[str, Any, None] = (bin(x)[2:] for x in sequence)
        string_binary_sequence: str = ", ".join(binary_sequence)

        logger.info(string_binary_sequence)

        end_time: float = (time.perf_counter() - start_time) * 1000

        logger.info("Продолжительность генерации %s мс", end_time)

        if not self._linear_congruent_service.is_maximized_period(linear_generator):
            logger.info("Последовательность не имеет период длиной m")

        start_time = time.perf_counter()

        period = self._linear_congruent_service.get_period(linear_generator)
        start_period_index = self._linear_congruent_service.get_start_period_index(linear_generator)

        end_time = (time.perf_counter() - start_time) * 1000

        logger.info("Период последовательности: %s", period)
        logger.info("Начало периода: %s", start_period_index)
        logger.info("Время поиска периода: %s мс", end_time)

        path_to_save: Path = Path(__file__).parent.parent.parent.parent.parent / "linear_congruent.txt"

        with open(path_to_save, "w", encoding="utf-8") as f:
            f.write(' '.join(map(str, sequence)))

        logger.info("Файл с параметрами генератора: %s", path_to_save)

