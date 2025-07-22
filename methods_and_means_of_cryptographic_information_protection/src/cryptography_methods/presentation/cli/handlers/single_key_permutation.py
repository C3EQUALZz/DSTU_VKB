import asyncio
import re

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.single_key_permutation.decrypt import (
    SingleKeyPermutationDecryptCommandHandler, SingleKeyPermutationDecryptCommand
)
from cryptography_methods.application.commands.single_key_permutation.encrypt import (
    SingleKeyPermutationEncryptCommandHandler,
    SingleKeyPermutationEncryptCommand
)
from cryptography_methods.application.common.views.single_key_permutation import (
    SingleKeyPermutationEncryptView,
    SingleKeyPermutationDecryptView
)


@click.group(name="single-key-permutation")
def single_key_permutation_group() -> None:
    ...


@single_key_permutation_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
@click.option("-c", "--columns", help="Number of columns for table", default=6, type=int)
@click.option("-r", "--rows", help="Number of rows for table", default=4, type=int)
def cmd_encrypt_handler(
        text: str,
        key: str,
        columns: int,
        rows: int,
        interactor: FromDishka[SingleKeyPermutationEncryptCommandHandler]
) -> None:
    if text.isspace() or text == "":
        click.echo("text cant be empty, please provide some info", err=True)
        return

    if bool(re.search(r'\d', text)):
        click.echo("text cant contain digits, please provide only letters", err=True)
        return

    if key.isspace() or key == "":
        click.echo("key cant be empty, please provide some info", err=True)
        return

    if bool(re.search(r'\d', key)):
        click.echo("key cant contain digits, please provide only letters", err=True)
        return

    if columns <= 0:
        click.echo("Number of columns cant be less than 0", err=True)
        return

    if rows <= 0:
        click.echo("Number of rows cant be less than 0", err=True)
        return

    command: SingleKeyPermutationEncryptCommand = SingleKeyPermutationEncryptCommand(
        width=columns,
        height=rows,
        data=text,
        key=key,
    )

    view: SingleKeyPermutationEncryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Single Key Permutation"
    table.field_names = ["original text", "encrypted text", "columns", "rows", "key"]
    table.add_row([view.original_text, view.encrypted_text, columns, rows, key])

    click.echo(table)


@single_key_permutation_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption", type=str)
@click.option("-c", "--columns", help="Number of columns for table", default=6, type=int)
@click.option("-r", "--rows", help="Number of rows for table", default=4, type=int)
def cmd_decrypt_handler(
        text: str,
        key: str,
        columns: int,
        rows: int,
        interactor: FromDishka[SingleKeyPermutationDecryptCommandHandler]
) -> None:
    if text.isspace() or text == "":
        click.echo("text cant be empty, please provide some info", err=True)
        return

    if bool(re.search(r'\d', text)):
        click.echo("text cant contain digits, please provide only letters", err=True)
        return

    if key.isspace() or key == "":
        click.echo("key cant be empty, please provide some info", err=True)
        return

    if bool(re.search(r'\d', key)):
        click.echo("key cant contain digits, please provide only letters", err=True)
        return

    if columns <= 0:
        click.echo("Number of columns cant be less than 0", err=True)
        return

    if rows <= 0:
        click.echo("Number of rows cant be less than 0", err=True)
        return

    command: SingleKeyPermutationDecryptCommand = SingleKeyPermutationDecryptCommand(
        width=columns,
        height=rows,
        data=text,
        key=key,
    )

    view: SingleKeyPermutationDecryptView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Single Key Permutation"
    table.field_names = ["original text", "decrypted text", "columns", "rows", "key"]
    table.add_row([view.original_text, view.decrypted_text, columns, rows, key])

    click.echo(table)
