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
    "--output-path",
    type=click.Path(path_type=Path),
    help="Path to save the distribution plot",
)
@click.option(
    "--show/--no-show",
    default=True,
    help="Whether to display the plot",
)
@click.option(
    "--desktop",
    is_flag=True,
    help="Use Desktop directory for default file paths",
)
def cmd_generate_handler(
    linear_congruent_file: Path | None,
    square_congruent_file: Path | None,
    fibonacci_file: Path | None,
    geffe_file: Path | None,
    output_path: Path | None,
    show: bool,
    desktop: bool,
    interactor: FromDishka[
        MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommandHandler
    ],
) -> None:
    """Generate plane distributions for PRNG sequences."""
    # If desktop flag is set, use default Desktop paths
    if desktop:
        desktop_path = Path.home() / "Desktop"
        if linear_congruent_file is None:
            linear_congruent_file = desktop_path / "LinearCongruent.txt"
        if square_congruent_file is None:
            square_congruent_file = desktop_path / "SquareCongruent.txt"
        if fibonacci_file is None:
            fibonacci_file = desktop_path / "Fibonacci.txt"
        if geffe_file is None:
            geffe_file = desktop_path / "Geffen.txt"
        if output_path is None:
            output_path = desktop_path / "plane_distribution.png"

    command = MethodologyForAssessingTheQualityOfGpspDistributionOnPlaneCommand(
        linear_congruent_file=linear_congruent_file,
        square_congruent_file=square_congruent_file,
        fibonacci_file=fibonacci_file,
        geffe_file=geffe_file,
        output_path=output_path,
        show=show,
    )

    try:
        interactor(command)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

