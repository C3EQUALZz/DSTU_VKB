"""CLI commands for Geffe generator."""

import click
from dishka import FromDishka

from theory_of_pseudorandom_generators.application.commands.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand,
    GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler,
)


@click.group(name="geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback")
def geffe_generator_group() -> None:
    """Geffe generator commands."""
    ...


@geffe_generator_group.command(name="generate")
@click.option(
    "-p1",
    "--register1-polynomial",
    required=True,
    help="Coefficients of primitive polynomial for register 1 (space-separated)",
    type=str,
)
@click.option(
    "-s1",
    "--register1-start-state",
    required=True,
    help="Initial register 1 state (space-separated)",
    type=str,
)
@click.option(
    "-k1",
    "--register1-shift",
    required=True,
    help="Shift value k for register 1",
    type=int,
)
@click.option(
    "-c1",
    "--register1-column-index",
    default=0,
    help="Column index for register 1",
    type=int,
)
@click.option(
    "-p2",
    "--register2-polynomial",
    required=True,
    help="Coefficients of primitive polynomial for register 2 (space-separated)",
    type=str,
)
@click.option(
    "-s2",
    "--register2-start-state",
    required=True,
    help="Initial register 2 state (space-separated)",
    type=str,
)
@click.option(
    "-k2",
    "--register2-shift",
    required=True,
    help="Shift value k for register 2",
    type=int,
)
@click.option(
    "-c2",
    "--register2-column-index",
    default=0,
    help="Column index for register 2",
    type=int,
)
@click.option(
    "-p3",
    "--register3-polynomial",
    required=True,
    help="Coefficients of primitive polynomial for register 3 (space-separated)",
    type=str,
)
@click.option(
    "-s3",
    "--register3-start-state",
    required=True,
    help="Initial register 3 state (space-separated)",
    type=str,
)
@click.option(
    "-k3",
    "--register3-shift",
    required=True,
    help="Shift value k for register 3",
    type=int,
)
@click.option(
    "-c3",
    "--register3-column-index",
    default=0,
    help="Column index for register 3",
    type=int,
)
@click.option(
    "-n",
    "--number-count",
    default=10,
    help="Number of decimal numbers to generate",
    type=int,
)
def cmd_generate_handler(
    register1_polynomial: str,
    register1_start_state: str,
    register1_shift: int,
    register1_column_index: int,
    register2_polynomial: str,
    register2_start_state: str,
    register2_shift: int,
    register2_column_index: int,
    register3_polynomial: str,
    register3_start_state: str,
    register3_shift: int,
    register3_column_index: int,
    number_count: int,
    interactor: FromDishka[
        GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommandHandler
    ],
) -> None:
    """Generate Geffe sequence."""
    try:
        reg1_poly = tuple(int(x) for x in register1_polynomial.split())
        reg1_state = tuple(int(x) for x in register1_start_state.split())
        reg2_poly = tuple(int(x) for x in register2_polynomial.split())
        reg2_state = tuple(int(x) for x in register2_start_state.split())
        reg3_poly = tuple(int(x) for x in register3_polynomial.split())
        reg3_state = tuple(int(x) for x in register3_start_state.split())

        command = GeffeyPseudorandomNumberGeneratorOnShiftRegistersWithLinearFeedbackCommand(
            register1_polynomial=reg1_poly,
            register1_start_state=reg1_state,
            register1_shift=register1_shift,
            register1_column_index=register1_column_index,
            register2_polynomial=reg2_poly,
            register2_start_state=reg2_state,
            register2_shift=register2_shift,
            register2_column_index=register2_column_index,
            register3_polynomial=reg3_poly,
            register3_start_state=reg3_state,
            register3_shift=register3_shift,
            register3_column_index=register3_column_index,
            number_count=number_count,
        )

        interactor(command)
    except ValueError as e:
        click.echo(f"Ошибка ввода: {e}", err=True)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)

