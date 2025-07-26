import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.vigenere.decrypt import (
    VigenereDecryptCommandHandler,
    VigenereDecryptCommand
)
from cryptography_methods.application.commands.vigenere.encrypt import (
    VigenereEncryptCommandHandler,
    VigenereEncryptCommand
)
from cryptography_methods.application.common.views.vigenere import (
    VigenereEncryptView,
    VigenereDecryptView
)


@click.group(name="vigenere")
def vigenere_group() -> None:
    ...


@vigenere_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
def cmd_encrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[VigenereEncryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key == "" or key.isspace():
        click.echo("Please provide any key, not space", err=True)
        return

    command: VigenereEncryptCommand = VigenereEncryptCommand(
        text=text,
        key=key,
    )

    view: VigenereEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Vigenere"
    table.field_names = [
        "original text",
        "encrypted text",
        "key",
        "length of alphabet"
    ]

    table.add_row([
        view.original_text,
        view.encrypted_text,
        view.key,
        view.length_of_alphabet
    ])

    click.echo(table)


@vigenere_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
def cmd_decrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[VigenereDecryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    if key == "" or key.isspace():
        click.echo("Please provide any key, not space", err=True)
        return

    command: VigenereDecryptCommand = VigenereDecryptCommand(
        text=text,
        key=key,
    )

    view: VigenereDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Vigenere"
    table.field_names = [
        "original text",
        "decrypted text",
        "key",
        "length of alphabet"
    ]

    table.add_row([
        view.original_text,
        view.decrypted_text,
        view.key,
        view.length_of_alphabet
    ])

    click.echo(table)
