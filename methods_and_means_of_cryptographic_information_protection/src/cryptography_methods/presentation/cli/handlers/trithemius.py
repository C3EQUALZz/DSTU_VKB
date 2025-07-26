import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.trithemius.decrypt import (
    TrithemiusDecryptCommandHandler,
    TrithemiusDecryptCommand
)
from cryptography_methods.application.commands.trithemius.encrypt import (
    TrithemiusEncryptCommandHandler,
    TrithemiusEncryptCommand
)
from cryptography_methods.application.common.views.trithemius import (
    TrithemiusEncryptView,
    TrithemiusDecryptView
)


@click.group(name="trithemius")
def trithemius_group() -> None:
    ...


@trithemius_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
@click.option("-c", "--columns", required=True, help="Number of columns for table", type=int)
@click.option("-r", "--rows", required=True, help="Number of rows for table", type=int)
def cmd_encrypt_handler(
        text: str,
        key: str,
        columns: int,
        rows: int,
        interactor: FromDishka[TrithemiusEncryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key == "" or key.isspace():
        click.echo("Please provide any key, not space", err=True)
        return

    if rows < 0 or columns < 0:
        click.echo("Please provide any number of columns and rows", err=True)
        return

    command: TrithemiusEncryptCommand = TrithemiusEncryptCommand(
        text=text,
        key=key,
        columns=columns,
        rows=rows,
    )

    view: TrithemiusEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Trithemius"
    table.field_names = [
        "original text",
        "encrypted text",
        "columns",
        "rows",
        "key",
        "length of alphabet"
    ]

    table.add_row([
        view.original_text,
        view.encrypted_text,
        view.width,
        view.height,
        view.key,
        view.length_of_alphabet
    ])

    click.echo(table)


@trithemius_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
@click.option("-c", "--columns", required=True, help="Number of columns for table", type=int)
@click.option("-r", "--rows", required=True, help="Number of rows for table", type=int)
def cmd_decrypt_handler(
        text: str,
        key: str,
        columns: int,
        rows: int,
        interactor: FromDishka[TrithemiusDecryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key == "" or key.isspace():
        click.echo("Please provide any key, not space", err=True)
        return

    if rows < 0 or columns < 0:
        click.echo("Please provide any number of columns and rows", err=True)
        return

    command: TrithemiusDecryptCommand = TrithemiusDecryptCommand(
        text=text,
        key=key,
        columns=columns,
        rows=rows,
    )

    view: TrithemiusDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Trithemius"
    table.field_names = [
        "original text",
        "decrypted text",
        "columns",
        "rows",
        "key",
        "length of alphabet"
    ]

    table.add_row([
        view.original_text,
        view.decrypted_text,
        view.width,
        view.height,
        view.key,
        view.length_of_alphabet
    ])

    click.echo(table)