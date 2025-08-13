import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.double_square_whitestone.decrypt import (
    DecryptDoubleSquareWhitestoneCommandHandler, DecryptDoubleSquareWhitestoneCommand
)
from cryptography_methods.application.commands.double_square_whitestone.encrypt import (
    EncryptDoubleSquareWhitestoneCommandHandler,
    EncryptDoubleSquareWhitestoneCommand
)
from cryptography_methods.application.common.views.double_square_whitestone import (
    DoubleSquareWhitestoneEncryptView,
    DoubleSquareWhitestoneDecryptView
)


@click.group(name="double_square_whitestone")
def double_square_whitestone_group() -> None:
    ...


@double_square_whitestone_group.command("encrypt")
@click.option("-key", "--keyword", required=False, help="Keyword for encryption", type=list[list[str]], default=None)
@click.option("-t", "--text", required=True, help="Text for encryption", type=str)
def cmd_encrypt_handler(
        text: str,
        key: list[list[str]] | None,
        interactor: FromDishka[EncryptDoubleSquareWhitestoneCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key is not None:
        if not all((symbol.isalpha() or symbol.isspace() or symbol in ":,.") for table in key for symbol in table):
            click.echo("All symbols must be alphas, not another", err=True)
            return

    command: EncryptDoubleSquareWhitestoneCommand = EncryptDoubleSquareWhitestoneCommand(
        text=text,
        key_for_encryption=key
    )

    view: DoubleSquareWhitestoneEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Double square Whitestone"
    table.field_names = [
        "original text",
        "encrypted text",
        "left table",
        "right table",
    ]
    table.add_row([
        view.text,
        view.encrypted_text,
        view.key_for_encryption[0],
        view.key_for_encryption[1],
    ])

    click.echo(table)


@double_square_whitestone_group.command("decrypt")
@click.option("-key", "--keyword", required=False, help="Keyword for decryption", type=list[list[str]], default=None)
@click.option("-t", "--text", required=True, help="Text for decryption", type=str)
def cmd_decrypt_handler(
        key: list[list[str]],
        text: str,
        interactor: FromDishka[DecryptDoubleSquareWhitestoneCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key is not None:
        if not all((symbol.isalpha() or symbol.isspace() or symbol in ":,.") for table in key for symbol in table):
            click.echo("All symbols must be alphas, not another", err=True)
            return

    command: DecryptDoubleSquareWhitestoneCommand = DecryptDoubleSquareWhitestoneCommand(
        text=text,
        key_for_decryption=key
    )

    view: DoubleSquareWhitestoneDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Double square Whitestone"
    table.field_names = [
        "original text",
        "decrypted text",
        "left table",
        "right table",
    ]
    table.add_row([
        view.text,
        view.decrypted_text,
        view.key_for_decryption[0],
        view.key_for_decryption[1],
    ])

    click.echo(table)
