import ast
import asyncio
import json
import string

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


@click.group(name="double-square-whitestone")
def double_square_whitestone_group() -> None:
    ...


@double_square_whitestone_group.command("encrypt")
@click.option("-lt", "--left-table", required=True, help="Left table for encryption", type=str)
@click.option("-rt", "--right-table", required=True, help="Right table for encryption", type=str)
@click.option("-t", "--text", required=True, help="Text for encryption", type=str)
def cmd_encrypt_handler(
        text: str,
        left_table: str,
        right_table: str,
        interactor: FromDishka[EncryptDoubleSquareWhitestoneCommandHandler]
) -> None:
    converted_left_table: list[list[str]] = ast.literal_eval(left_table)

    if not all(
            (column.isalpha() or column.isspace() or column in string.punctuation)
            for row in converted_left_table for column in row
    ):
        click.echo("All symbols must be alphas, not another", err=True)
        return

    converted_right_table: list[list[str]] = ast.literal_eval(right_table)

    if not all(
            (column.isalpha() or column.isspace() or column in string.punctuation)
            for row in converted_right_table for column in row
    ):
        click.echo("All symbols must be alphas, not another", err=True)
        return

    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    command: EncryptDoubleSquareWhitestoneCommand = EncryptDoubleSquareWhitestoneCommand(
        text=text,
        left_table=converted_left_table,
        right_table=converted_right_table,
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
        view.left_table,
        view.right_table,
    ])

    click.echo(table)


@double_square_whitestone_group.command("decrypt")
@click.option("-lt", "--left-table", required=True, help="Left table for decryption", type=str)
@click.option("-rt", "--right-table", required=True, help="Right table for decryption", type=str)
@click.option("-t", "--text", required=True, help="Text for decryption", type=str)
def cmd_decrypt_handler(
        text: str,
        left_table: str,
        right_table: str,
        interactor: FromDishka[DecryptDoubleSquareWhitestoneCommandHandler]
) -> None:
    converted_left_table: list[list[str]] = ast.literal_eval(left_table)

    if not all(
            (column in string.punctuation + string.ascii_letters or column.isalpha())
            for row in converted_left_table for column in row
    ):
        click.echo("All symbols must be alphas, not another", err=True)
        return

    converted_right_table: list[list[str]] = ast.literal_eval(right_table)

    if not all(
            (column in string.punctuation + string.ascii_letters or column.isalpha())
            for row in converted_right_table for column in row
    ):
        click.echo("All symbols must be alphas, not another", err=True)
        return

    if text == "" or text.isspace():
        click.echo("Please provide any text, not space", err=True)
        return

    command: DecryptDoubleSquareWhitestoneCommand = DecryptDoubleSquareWhitestoneCommand(
        text=text,
        left_table=converted_left_table,
        right_table=converted_right_table,
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
        view.left_table,
        view.right_table,
    ])

    click.echo(table)
