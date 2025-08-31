import asyncio
import json
import pickle

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.magic_table.decrypt import (
    MagicTableDecryptCommandHandler,
    MagicTableDecryptCommand
)
from cryptography_methods.application.commands.magic_table.encrypt import (
    MagicTableEncryptCommandHandler,
    MagicTableEncryptCommand
)
from cryptography_methods.application.common.views.magic_table import (
    MagicTableEncryptView,
    MagicTableDecryptView
)


@click.group(name="magic-table")
def magic_table_group() -> None:
    ...


@magic_table_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
def cmd_encrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[MagicTableEncryptCommandHandler]
) -> None:
    parsed_keys: list[list[int]] = json.loads(key)

    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    command: MagicTableEncryptCommand = MagicTableEncryptCommand(
        text=text,
        table=parsed_keys
    )

    view: MagicTableEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Magic Table"
    table.field_names = [
        "original text",
        "encrypted text",
        "key",
    ]
    table.add_row([
        view.text,
        view.encrypted_text,
        view.magic_table
    ])

    click.echo(table)


@magic_table_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to decrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for decryption", type=str)
def cmd_decrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[MagicTableDecryptCommandHandler]
) -> None:
    parsed_keys: list[list[int]] = json.loads(key)

    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    command: MagicTableDecryptCommand = MagicTableDecryptCommand(
        text=text,
        table=parsed_keys
    )

    view: MagicTableDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Magic Table"
    table.field_names = [
        "original text",
        "decrypted text",
        "key"
    ]
    table.add_row([
        view.text,
        view.decrypted_text,
        view.magic_table
    ])

    click.echo(table)
