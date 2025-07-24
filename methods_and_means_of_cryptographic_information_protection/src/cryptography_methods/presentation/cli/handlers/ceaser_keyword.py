import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.ceaser_keyword.decrypt import (
    CeaserKeywordDecryptCommandHandler,
    CeaserKeywordDecryptCommand
)
from cryptography_methods.application.commands.ceaser_keyword.encrypt import (
    CeaserKeywordEncryptCommandHandler,
    CeaserKeywordEncryptCommand
)
from cryptography_methods.application.common.views.ceaser_keyword import (
    CeaserKeywordEncryptionView,
    CeaserKeywordDecryptionView
)


@click.group(name="ceaser-keyword")
def ceaser_keyword_group() -> None:
    ...


@ceaser_keyword_group.command("encrypt")
@click.option("-k", "--k", required=True, help="Number for key encryption", type=int)
@click.option("-keyw", "--keyword", required=True, help="Keyword for encryption", type=str)
@click.option("-t", "--text", required=True, help="Text for encryption", type=str)
def cmd_encrypt_handler(
        k: int,
        keyword: str,
        text: str,
        interactor: FromDishka[CeaserKeywordEncryptCommandHandler]
) -> None:
    stripped_keyword: str = keyword.strip()
    stripped_text: str = text.strip()

    if ((
            stripped_keyword.isupper() and stripped_text.islower()
    ) or (
            stripped_keyword.islower() and stripped_text.isupper()
    )):
        click.echo("Different cases for keyword and key")
        return

    if k < 0:
        click.echo("k cannot be negative")
        return

    if any(char.isspace() for char in stripped_keyword):
        click.echo("keyword cannot contains space")
        return

    if stripped_text.isspace() or stripped_text == "":
        click.echo("text cannot be empty")
        return

    if stripped_text.isnumeric():
        click.echo("text cannot be numeric")
        return

    if stripped_keyword.isspace() or stripped_keyword == "":
        click.echo("keyword cannot be empty")
        return

    if stripped_keyword.isnumeric():
        click.echo("keyword cannot be numeric")
        return

    command: CeaserKeywordEncryptCommand = CeaserKeywordEncryptCommand(
        k=k,
        keyword=stripped_keyword,
        text=stripped_text,
    )

    view: CeaserKeywordEncryptionView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Ceaser Keyword"
    table.field_names = ["original text", "encrypted text", "keyword", "m", "k"]
    table.add_row([view.original_text, view.encrypted_text, view.keyword, view.m, view.k])

    click.echo(table)


@ceaser_keyword_group.command("decrypt")
@click.option("-k", "--k", required=True, help="Number for key decryption", type=int)
@click.option("-keyw", "--keyword", required=True, help="Keyword for decryption", type=str)
@click.option("-t", "--text", required=True, help="Text for decryption", type=str)
def cmd_decrypt_handler(
        k: int,
        keyword: str,
        text: str,
        interactor: FromDishka[CeaserKeywordDecryptCommandHandler]
) -> None:
    stripped_keyword: str = keyword.strip()
    stripped_text: str = text.strip()

    if ((
            stripped_keyword.isupper() and stripped_text.islower()
    ) or (
            stripped_keyword.islower() and stripped_text.isupper()
    )):
        click.echo("Different cases for keyword and key")
        return

    if k < 0:
        click.echo("k cannot be negative")
        return

    if any(char.isspace() for char in stripped_keyword):
        click.echo("keyword cannot contains space")
        return

    if stripped_text.isspace() or stripped_text == "":
        click.echo("text cannot be empty")
        return

    if stripped_text.isnumeric():
        click.echo("text cannot be numeric")
        return

    if stripped_keyword.isspace() or stripped_keyword == "":
        click.echo("keyword cannot be empty")
        return

    if stripped_keyword.isnumeric():
        click.echo("keyword cannot be numeric")
        return

    command: CeaserKeywordDecryptCommand = CeaserKeywordDecryptCommand(
        k=k,
        keyword=stripped_keyword,
        text=stripped_text,
    )

    view: CeaserKeywordDecryptionView = asyncio.run(interactor(command))

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Ceaser Keyword"
    table.field_names = ["original text", "decrypted text", "keyword", "m", "k"]
    table.add_row([view.original_text, view.decrypted_text, view.keyword, view.m, view.k])

    click.echo(table)
