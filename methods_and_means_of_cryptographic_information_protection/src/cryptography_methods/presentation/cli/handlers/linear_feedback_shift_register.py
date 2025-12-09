import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.linear_feedback_shift_register.mutate import (
    MutateLinearFeedbackShiftRegisterCommandHandler, MutateLinearFeedbackShiftRegisterCommand
)
from cryptography_methods.domain.linear_feedback_shift_register.services.linear_feedback_shift_register_service import (
    LinearFeedbackShiftRegisterSequencePeriodDTO
)


@click.group(name="linear-feedback-shift")
def linear_feedback_group() -> None:
    ...


@linear_feedback_group.command("mutate")
@click.option("-s", "--sequence", required=True, help="Sequence for initial mutation", type=str)
@click.option("-p", "--polynom", required=True, help="Polynom which describes mutation", type=str)
def cmd_mutate_handler(
        sequence: str,
        polynom: str,
        interactor: FromDishka[MutateLinearFeedbackShiftRegisterCommandHandler]
) -> None:
    command: MutateLinearFeedbackShiftRegisterCommand = MutateLinearFeedbackShiftRegisterCommand(
        sequence=sequence,
        polynom=polynom,
    )

    view: LinearFeedbackShiftRegisterSequencePeriodDTO = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()

    table.title = "Mutation Result - LFSR"
    table.field_names = [
        "initial sequence",
        "polynom",
        "period",
        "output_sequence"
    ]
    table.add_row([
        sequence,
        polynom,
        view.period,
        view.output_sequence
    ])

    click.echo(table)
