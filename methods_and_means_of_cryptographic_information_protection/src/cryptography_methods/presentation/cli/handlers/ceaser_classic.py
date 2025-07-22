import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.ceaser_classic.decrypt import (
    CeaserClassicDecryptCommandHandler,
    CeaserClassicDecryptCommand
)
from cryptography_methods.application.commands.ceaser_classic.encrypt import (
    CeaserClassicEncryptCommandHandler,
    CeaserClassicEncryptCommand
)
from cryptography_methods.application.common.views.ceaser_classic import (
    CeaserClassicEncryptionView,
    CeaserClassicDecryptionView
)


@click.group(name="ceaser-classic")
def ceaser_classic_group() -> None:
    ...


@ceaser_classic_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", help="Key for encryption", type=int)
def cmd_encrypt_handler(
        text: str,
        key: int,
        interactor: FromDishka[CeaserClassicEncryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("You need to enter a text")
        return

    if key <= 0:
        click.echo("You need to enter a positive integer")
        return

    command: CeaserClassicEncryptCommand = CeaserClassicEncryptCommand(
        key=key,
        text=text.strip()
    )

    view: CeaserClassicEncryptionView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Ceaser Classic Encryption"
    table.field_names = ["original text", "encrypted text", "key"]
    table.add_row([view.original_text, view.encrypted_text, view.key])

    click.echo(table)


@ceaser_classic_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", help="Key for encryption", type=int)
def cmd_decrypt_handler(
        text: str,
        key: int,
        interactor: FromDishka[CeaserClassicDecryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("You need to enter a text")
        return

    if key <= 0:
        click.echo("You need to enter a positive integer")
        return

    command: CeaserClassicDecryptCommand = CeaserClassicDecryptCommand(
        key=key,
        text=text.strip()
    )

    view: CeaserClassicDecryptionView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Ceaser Classic Encryption"
    table.field_names = ["original text", "decrypted text", "key"]
    table.add_row([view.original_text, view.decrypted_text, view.key])

    click.echo(table)
