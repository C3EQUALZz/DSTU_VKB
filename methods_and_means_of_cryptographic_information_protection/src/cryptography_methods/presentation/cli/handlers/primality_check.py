import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.primality_check.check import (
    PrimalityCheckCommand,
    PrimalityCheckCommandHandler,
)
from cryptography_methods.application.common.views.primality_check import (
    PrimalityCheckView,
)


@click.group(name="primality-check")
def primality_check_group() -> None:
    ...


@primality_check_group.command("check")
@click.option(
    "-n",
    "--number",
    required=True,
    help="Число для проверки на простоту",
    type=int,
)
@click.option(
    "-k",
    "--iterations",
    default=20,
    help="Количество итераций теста Миллера-Рабина",
    type=int,
)
def cmd_check_handler(
    number: int,
    iterations: int,
    interactor: FromDishka[PrimalityCheckCommandHandler],
) -> None:
    if number < 2:  # noqa: PLR2004
        click.echo("Число должно быть >= 2")
        return

    if iterations <= 0:
        click.echo("Количество итераций должно быть положительным")
        return

    command: PrimalityCheckCommand = PrimalityCheckCommand(
        number=number,
        iterations=iterations,
    )

    view: PrimalityCheckView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Проверка на простоту — тест Миллера-Рабина"
    table.field_names = ["число", "простое?", "итерации"]
    table.add_row([
        view.number,
        "Да" if view.is_prime else "Нет",
        view.iterations,
    ])

    click.echo(table)
