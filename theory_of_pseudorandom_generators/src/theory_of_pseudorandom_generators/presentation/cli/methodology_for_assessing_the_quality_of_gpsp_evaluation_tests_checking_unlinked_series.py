"""CLI commands for NIST tests."""

from pathlib import Path

import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series import (
    MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommand,
    MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommandHandler,
)


@click.group(name="methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series")
def nist_tests_group() -> None:
    """NIST tests commands."""


@nist_tests_group.command(name="run")
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
    "-m",
    "--block-size",
    required=True,
    type=int,
    help="Block size parameter (m)",
)
@click.option(
    "-a",
    "--alpha",
    default=0.01,
    type=float,
    help="Significance level (default: 0.01)",
)
@click.option(
    "--desktop",
    is_flag=True,
    help="Use Desktop directory for default file paths",
)
def cmd_run_handler(
    linear_congruent_file: Path | None,
    square_congruent_file: Path | None,
    fibonacci_file: Path | None,
    geffe_file: Path | None,
    block_size: int,
    alpha: float,
    desktop: bool,
    interactor: FromDishka[
        MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommandHandler
    ],
) -> None:
    """Run NIST tests on PRNG sequences."""
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

    command = MethodologyForAssessingTheQualityOfGpspEvaluationTestsCheckingUnlinkedSeriesCommand(
        linear_congruent_file=linear_congruent_file,
        square_congruent_file=square_congruent_file,
        fibonacci_file=fibonacci_file,
        geffe_file=geffe_file,
        block_size=block_size,
        alpha=alpha,
    )

    try:
        interactor(command)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

