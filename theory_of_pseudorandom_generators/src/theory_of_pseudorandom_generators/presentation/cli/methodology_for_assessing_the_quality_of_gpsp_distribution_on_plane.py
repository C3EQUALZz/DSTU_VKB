"""CLI commands for plane distribution generation."""

from pathlib import Path

import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane import (
    MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommand,
    MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler,
)


@click.group(name="methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane")
def plane_distribution_group() -> None:
    """Plane distribution generation commands."""


@plane_distribution_group.command(name="generate")
@click.option(
    "--linear-congruent-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to linear congruent generator sequence file",
)
@click.option(
    "--square-congruent-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to square congruent generator sequence file",
)
@click.option(
    "--fibonacci-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to Fibonacci generator sequence file",
)
@click.option(
    "--geffe-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to Geffe generator sequence file",
)
@click.option(
    "--show/--no-show",
    default=True,
    help="Whether to display the plot",
)
def cmd_generate_handler(
    linear_congruent_file: Path,
    square_congruent_file: Path,
    fibonacci_file: Path,
    geffe_file: Path,
    show: bool,
    interactor: FromDishka[
        MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler
    ],
) -> None:
    """Generate plane distributions for PRNG sequences."""

    command = MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommand(
        linear_congruent_file=linear_congruent_file,
        square_congruent_file=square_congruent_file,
        fibonacci_file=fibonacci_file,
        geffe_file=geffe_file,
        show=show,
    )

    try:
        interactor(command)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

