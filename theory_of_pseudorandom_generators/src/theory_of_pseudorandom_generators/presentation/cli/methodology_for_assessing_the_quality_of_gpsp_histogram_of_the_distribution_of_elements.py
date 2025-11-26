"""CLI команды для построения гистограмм распределения элементов."""

from pathlib import Path

import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements import (
    MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommand,
    MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommandHandler,
)


@click.group(
    name="methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements",
)
def histogram_group() -> None:
    """Команды для построения гистограмм распределения элементов."""


@histogram_group.command(name="generate")
@click.option(
    "--linear-congruent-file",
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу с последовательностью линейного конгруэнтного генератора",
)
@click.option(
    "--square-congruent-file",
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу с последовательностью квадратичного конгруэнтного генератора",
)
@click.option(
    "--fibonacci-file",
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу с последовательностью генератора Фибоначчи",
)
@click.option(
    "--geffe-file",
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу с последовательностью генератора Геффе",
)
@click.option(
    "--show/--no-show",
    default=True,
    help="Показывать ли гистограммы на экране",
)
def cmd_generate_handler(
    linear_congruent_file: Path,
    square_congruent_file: Path,
    fibonacci_file: Path,
    geffe_file: Path,
    show: bool,
    interactor: FromDishka[
        MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommandHandler
    ],
) -> None:
    """Построить гистограммы распределения элементов для различных ГПСЧ."""

    command = MethodologyForAssessingTheQualityOfGpspHistogramOfTheDistributionOfElementsCommand(
        linear_congruent_file=linear_congruent_file,
        square_congruent_file=square_congruent_file,
        fibonacci_file=fibonacci_file,
        geffe_file=geffe_file,
        show=show,
    )

    try:
        interactor(command)
    except Exception as e:  # noqa: BLE001
        click.echo(f"Ошибка: {e}", err=True)



