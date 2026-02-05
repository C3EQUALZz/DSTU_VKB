import asyncio
import secrets

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.gost_28147.decrypt import (
    Gost28147DecryptCommandHandler,
    Gost28147DecryptCommand
)
from cryptography_methods.application.commands.gost_28147.encrypt import (
    Gost28147EncryptCommandHandler,
    Gost28147EncryptCommand
)
from cryptography_methods.application.common.views.gost_28147 import (
    Gost28147EncryptionView,
    Gost28147DecryptionView
)


@click.group(name="gost-28147")
def gost_28147_group() -> None:
    """GOST 28147-89 encryption/decryption commands."""
    ...


@gost_28147_group.command("encrypt")
@click.option("-t", "--text", required=True, help="Text to encrypt", type=str)
@click.option("-k", "--key", required=True, help="Key for encryption (must be 32 bytes when encoded in UTF-8)", type=str)
def cmd_encrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[Gost28147EncryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("You need to enter a text")
        return

    if key == "" or key.isspace():
        click.echo("You need to enter a key")
        return

    command: Gost28147EncryptCommand = Gost28147EncryptCommand(
        text=text.strip(),
        key=key
    )

    try:
        view: Gost28147EncryptionView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "Encryption Result - GOST 28147-89"
        table.field_names = ["original text", "encrypted text (hex)", "key"]
        table.add_row([view.original_text, view.encrypted_text_hex, view.key])

        click.echo(table)
    except Exception as e:
        click.echo(f"Error during encryption: {e}")


@gost_28147_group.command("decrypt")
@click.option("-t", "--text", required=True, help="Encrypted text in hex format", type=str)
@click.option("-k", "--key", required=True, help="Key for decryption (must be 32 bytes when encoded in UTF-8)", type=str)
def cmd_decrypt_handler(
        text: str,
        key: str,
        interactor: FromDishka[Gost28147DecryptCommandHandler]
) -> None:
    if text == "" or text.isspace():
        click.echo("You need to enter a text")
        return

    if key == "" or key.isspace():
        click.echo("You need to enter a key")
        return

    command: Gost28147DecryptCommand = Gost28147DecryptCommand(
        text=text.strip(),
        key=key
    )

    try:
        view: Gost28147DecryptionView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "Decryption Result - GOST 28147-89"
        table.field_names = ["original text", "decrypted text", "key"]
        table.add_row([view.original_text, view.decrypted_text, view.key])

        click.echo(table)
    except Exception as e:
        click.echo(f"Error during decryption: {e}")


@gost_28147_group.command("generate-key")
def cmd_generate_key_handler() -> None:
    """Generate a random 32-byte key for GOST 28147-89."""
    random_bytes = secrets.token_bytes(32)
    
    try:
        key_string = random_bytes.decode('utf-8', errors='replace')
        click.echo(f"Generated key (32 bytes): {key_string!r}")
        click.echo(f"Key as hex: {random_bytes.hex()}")
    except Exception as e:
        click.echo(f"Error generating key: {e}")

