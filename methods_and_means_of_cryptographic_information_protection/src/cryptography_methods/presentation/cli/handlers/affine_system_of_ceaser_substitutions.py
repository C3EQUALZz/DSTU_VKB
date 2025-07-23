import asyncio

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.affine_system_of_ceaser_substitutions.decrypt import (
    AffineSystemOfCeaserSubstitutionDecryptCommandHandler,
    AffineSystemOfCeaserSubstitutionDecryptCommand
)
from cryptography_methods.application.commands.affine_system_of_ceaser_substitutions.encrypt import (
    AffineSystemOfCeaserSubstitutionEncryptCommandHandler,
    AffineSystemOfCeaserSubstitutionEncryptCommand
)
from cryptography_methods.application.common.views.affine_system_of_ceaser_substitution import (
    AffineSystemOfCeaserSubstitutionEncryptionView,
    AffineSystemOfCeaserSubstitutionDecryptionView
)


@click.group(name="affine-system-of-ceaser-substitutions")
def affine_system_of_ceaser_substitutions_group() -> None:
    ...


@affine_system_of_ceaser_substitutions_group.command("encrypt")
@click.option("-a", "--a", required=True, help="First parameter for key", type=int)
@click.option("-b", "--b", required=True, help="Second parameter for key", type=int)
@click.option("-t", "--text", required=True, help="Text for encryption", type=str)
def cmd_encrypt_handler(
        a: int,
        b: int,
        text: str,
        interactor: FromDishka[AffineSystemOfCeaserSubstitutionEncryptCommandHandler]
) -> None:
    if a < 0:
        click.echo("'a' cannot be negative", err=True)
        return

    if b < 0:
        click.echo("'b' cannot be negative", err=True)
        return

    if text.isspace() or text == "":
        click.echo("Please provide a text for encryption", err=True)
        return

    command: AffineSystemOfCeaserSubstitutionEncryptCommand = AffineSystemOfCeaserSubstitutionEncryptCommand(
        a=a,
        b=b,
        text=text
    )

    view: AffineSystemOfCeaserSubstitutionEncryptionView = asyncio.run(
        interactor(command)
    )

    table: PrettyTable = PrettyTable()
    table.title = "Encryption Result - Affine system of ceaser substitution"
    table.field_names = ["original text", "encrypted text", "a", "b", "m"]
    table.add_row([view.original_text, view.encrypted_text, view.a, view.b, view.m])

    click.echo(table)


@affine_system_of_ceaser_substitutions_group.command("decrypt")
@click.option("-a", "--a", required=True, help="First parameter for key", type=int)
@click.option("-b", "--b", required=True, help="Second parameter for key", type=int)
@click.option("-t", "--text", required=True, help="Text for decryption", type=str)
def cmd_decrypt_handler(
        a: int,
        b: int,
        text: str,
        interactor: FromDishka[AffineSystemOfCeaserSubstitutionDecryptCommandHandler]
) -> None:
    if a < 0:
        click.echo("'a' cannot be negative", err=True)
        return

    if b < 0:
        click.echo("'b' cannot be negative", err=True)
        return

    if text.isspace() or text == "":
        click.echo("Please provide a text for encryption", err=True)
        return

    command: AffineSystemOfCeaserSubstitutionDecryptCommand = AffineSystemOfCeaserSubstitutionDecryptCommand(
        a=a,
        b=b,
        text=text
    )

    view: AffineSystemOfCeaserSubstitutionDecryptionView = asyncio.run(
        interactor(command)
    )

    table: PrettyTable = PrettyTable()
    table.title = "Decryption Result - Affine system of ceaser substitution"
    table.field_names = ["original text", "decrypted text", "a", "b", "m"]
    table.add_row([view.original_text, view.decrypted_text, view.a, view.b, view.m])

    click.echo(table)
