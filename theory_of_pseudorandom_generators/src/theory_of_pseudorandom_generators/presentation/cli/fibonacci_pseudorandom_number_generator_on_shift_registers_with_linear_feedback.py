"""CLI commands for Fibonacci generator."""

import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
)


@click.group(name="fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback")
def fibonacci_generator_group() -> None:
    """Fibonacci generator commands."""


@fibonacci_generator_group.command(name="generate")
@click.option(
    "-p",
    "--polynomial",
    required=True,
    help="Coefficients of primitive polynomial (space-separated)",
    type=str,
)
@click.option(
    "-s",
    "--start-state",
    required=True,
    help="Initial register state (space-separated)",
    type=str,
)
@click.option(
    "-k",
    "--shift",
    required=True,
    help="Shift value k",
    type=int,
)
@click.option(
    "-c",
    "--column-index",
    default=0,
    help="Column index",
    type=int,
)
def cmd_generate_handler(
    polynomial: str,
    start_state: str,
    shift: int,
    column_index: int,
    interactor: FromDishka[
        FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler
    ],
) -> None:
    """Generate Fibonacci sequence."""
    try:
        poly_coeffs = tuple(int(x) for x in polynomial.split())
        start_state_values = tuple(int(x) for x in start_state.split())

        command = FibonacciPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand(
            polynomial_coefficients=poly_coeffs,
            start_state=start_state_values,
            shift=shift,
            column_index=column_index,
        )

        interactor(command)
    except ValueError as e:
        click.echo(f"Ошибка ввода: {e}", err=True)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

