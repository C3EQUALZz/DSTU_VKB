"""CLI handlers for ElGamal encryption and decryption."""
import asyncio
from pathlib import Path

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.elgamal.decrypt import (
    ElGamalDecryptCommand,
    ElGamalDecryptCommandHandler,
)
from cryptography_methods.application.commands.elgamal.encrypt import (
    ElGamalEncryptCommand,
    ElGamalEncryptCommandHandler,
)
from cryptography_methods.application.commands.elgamal.generate_keys import (
    ElGamalGenerateKeysCommand,
    ElGamalGenerateKeysCommandHandler,
)
from cryptography_methods.application.common.views.elgamal import (
    ElGamalDecryptionView,
    ElGamalEncryptionView,
    ElGamalKeyGenerationView,
)


@click.group(name="elgamal")
def elgamal_group() -> None:
    """ElGamal public-key cryptosystem commands."""
    ...


@elgamal_group.command("generate-keys")
@click.option(
    "-p",
    "--public-key-file",
    required=True,
    help="Path to save ElGamal public key file",
    type=click.Path(path_type=Path),
)
@click.option(
    "-pr",
    "--private-key-file",
    required=True,
    help="Path to save ElGamal private key file",
    type=click.Path(path_type=Path),
)
@click.option(
    "-s",
    "--key-size",
    default=1024,
    help="Size of ElGamal prime in bits (default: 1024)",
    type=int,
)
@click.option(
    "-c",
    "--prime-certainty",
    default=10,
    help="Miller–Rabin iterations for prime testing (default: 10)",
    type=int,
)
def cmd_generate_keys_handler(
    public_key_file: Path,
    private_key_file: Path,
    key_size: int,
    prime_certainty: int,
    interactor: FromDishka[ElGamalGenerateKeysCommandHandler],
) -> None:
    """Generate ElGamal key pair and save to files."""
    if key_size <= 0:
        click.echo("Error: key-size must be positive", err=True)
        raise click.Abort()

    if prime_certainty <= 0:
        click.echo("Error: prime-certainty must be positive", err=True)
        raise click.Abort()

    command: ElGamalGenerateKeysCommand = ElGamalGenerateKeysCommand(
        public_key_file=public_key_file,
        private_key_file=private_key_file,
        key_size=key_size,
        prime_certainty=prime_certainty,
    )

    try:
        view: ElGamalKeyGenerationView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "ElGamal Key Generation Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Key Size", f"{view.key_size} bits"])
        table.add_row(["Prime p (bits)", str(view.p_bits)])
        table.add_row(["Generator g", str(view.g)])
        table.add_row(["y (bits)", str(view.y_bits)])
        table.add_row(["Public Key File", view.public_key_file])
        table.add_row(["Private Key File", view.private_key_file])

        click.echo(table)
        click.echo("\n✓ ElGamal keys generated and saved successfully!")

    except Exception as e:
        click.echo(f"Error during ElGamal key generation: {e}", err=True)
        raise click.Abort() from e


@elgamal_group.command("encrypt")
@click.option(
    "-m",
    "--message",
    required=True,
    help="Message to encrypt",
    type=str,
)
@click.option(
    "-o",
    "--output-file",
    help="Path to save ElGamal ciphertext (message, a b pairs). Default: ./elgamal.txt",
    type=click.Path(path_type=Path),
    default=Path("elgamal.txt"),
    show_default=True,
)
@click.option(
    "-k",
    "--public-key-file",
    required=True,
    help="Path to ElGamal public key file",
    type=click.Path(exists=True, path_type=Path),
)
def cmd_encrypt_handler(
    message: str,
    public_key_file: Path,
    output_file: Path,
    interactor: FromDishka[ElGamalEncryptCommandHandler],
) -> None:
    """Encrypt a message using ElGamal algorithm."""
    if not message or message.isspace():
        click.echo("Error: Message cannot be empty", err=True)
        return

    command: ElGamalEncryptCommand = ElGamalEncryptCommand(
        message=message.strip(),
        public_key_file=public_key_file,
        output_file=output_file,
    )

    try:
        view: ElGamalEncryptionView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "ElGamal Encryption Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Original Message", view.original_message])
        table.add_row(["Prime p (bits)", str(view.p_bits)])
        table.add_row(["Ciphertext Pairs Count", str(view.ciphertext_pairs_count)])
        table.add_row(["Output File", view.output_file])

        click.echo(table)
        click.echo(f"\n✓ ElGamal data saved to: {view.output_file}")

    except Exception as e:
        click.echo(f"Error during ElGamal encryption: {e}", err=True)
        raise click.Abort() from e


@elgamal_group.command("decrypt")
@click.option(
    "-k",
    "--private-key-file",
    help="Path to ElGamal private key file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    "-i",
    "--input-file",
    help="Path to ElGamal data file (p, x, message, ciphertext). Default: ./elgamal.txt",
    type=click.Path(exists=True, path_type=Path),
    default=Path("elgamal.txt"),
    show_default=True,
)
def cmd_decrypt_handler(
    private_key_file: Path,
    input_file: Path,
    interactor: FromDishka[ElGamalDecryptCommandHandler],
) -> None:
    """Decrypt a message from file using ElGamal algorithm."""
    command: ElGamalDecryptCommand = ElGamalDecryptCommand(
        private_key_file=private_key_file,
        input_file=input_file,
    )

    try:
        view: ElGamalDecryptionView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "ElGamal Decryption Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Decrypted Message", view.decrypted_message])
        table.add_row(["Original Message (from file)", view.original_message_from_file])
        table.add_row(["Ciphertext Pairs Count", str(view.ciphertext_pairs_count)])
        table.add_row(["Input File", view.input_file])

        click.echo(table)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
    except ValueError as e:
        click.echo(f"Error: Invalid ElGamal file format - {e}", err=True)
        raise click.Abort() from e
    except Exception as e:
        click.echo(f"Error during ElGamal decryption: {e}", err=True)
        raise click.Abort() from e


