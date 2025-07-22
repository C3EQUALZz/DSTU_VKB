import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.simple_table_permutation.decrypt import (
    SimpleTablePermutationDecryptCommandHandler,
    SimpleTablePermutationDecryptCommand
)

from cryptography_methods.application.commands.simple_table_permutation.encrypt import (
    SimpleTablePermutationEncryptCommandHandler,
    SimpleTablePermutationEncryptCommand
)
from cryptography_methods.application.common.views.simple_table_permutation import (
    SimpleTablePermutationEncryptView,
    SimpleTablePermutationDecryptView
)


@click.group(name="simple-data-permutation")
def simple_data_permutation_group() -> None:
    ...


@simple_data_permutation_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-c", "--columns", help="Number of columns for table", default=6, type=int)
@click.option("-r", "--rows", help="Number of rows for table", default=4, type=int)
def cmd_encrypt_handler(
        text: str,
        columns: int,
        rows: int,
        interactor: FromDishka[SimpleTablePermutationEncryptCommandHandler]
) -> None:
    if columns <= 0:
        click.echo("Number of columns cant be less than 0", err=True)
        return

    if rows <= 0:
        click.echo("Number of rows cant be less than 0", err=True)
        return

    command: SimpleTablePermutationEncryptCommand = SimpleTablePermutationEncryptCommand(
        width=columns,
        height=rows,
        data=text
    )

    view: SimpleTablePermutationEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Simple Table Permutation"
    table.field_names = ["original text", "encrypted text", "columns", "rows"]
    table.add_row([view.original_text, view.encrypted_text, columns, rows])

    click.echo(table)


@simple_data_permutation_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-c", "--columns", help="Number of columns for table", default=6, type=int)
@click.option("-r", "--rows", help="Number of rows for table", default=4, type=int)
def cmd_decrypt_handler(
        text: str,
        columns: int,
        rows: int,
        interactor: FromDishka[SimpleTablePermutationDecryptCommandHandler]
) -> None:
    if columns <= 0:
        click.echo("Number of columns cant be less than 0", err=True)
        return

    if rows <= 0:
        click.echo("Number of rows cant be less than 0", err=True)
        return

    command: SimpleTablePermutationDecryptCommand = SimpleTablePermutationDecryptCommand(
        width=columns,
        height=rows,
        data=text
    )

    view: SimpleTablePermutationDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Simple Table Permutation"
    table.field_names = ["original text", "decrypted text", "columns", "rows"]
    table.add_row([view.original_text, view.decrypted_text, columns, rows])

    click.echo(table)
