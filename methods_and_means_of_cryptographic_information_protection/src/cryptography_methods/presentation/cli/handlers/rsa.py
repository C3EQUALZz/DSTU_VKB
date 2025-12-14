"""CLI handlers for RSA encryption and decryption."""
import asyncio
from pathlib import Path

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.rsa.decrypt import (
    RSADecryptCommand,
    RSADecryptCommandHandler,
)
from cryptography_methods.application.commands.rsa.encrypt import (
    RSAEncryptCommand,
    RSAEncryptCommandHandler,
)
from cryptography_methods.application.commands.rsa.generate_keys import (
    RSAGenerateKeysCommand,
    RSAGenerateKeysCommandHandler,
)
from cryptography_methods.application.common.views.rsa import (
    RSADecryptionView,
    RSAEncryptionView,
    RSAKeyGenerationView,
)


@click.group(name="rsa")
def rsa_group() -> None:
    """RSA encryption/decryption commands."""
    ...


@rsa_group.command("generate-keys")
@click.option(
    "-p",
    "--public-key-file",
    required=True,
    help="Path to save public key file",
    type=click.Path(path_type=Path),
)
@click.option(
    "-pr",
    "--private-key-file",
    required=True,
    help="Path to save private key file",
    type=click.Path(path_type=Path),
)
@click.option(
    "-s",
    "--key-size",
    default=2048,
    help="Size of RSA key in bits (default: 2048)",
    type=int,
)
@click.option(
    "-d",
    "--min-prime-diff-bits",
    default=64,
    help="Minimum difference between primes in bits (default: 64)",
    type=int,
)
def cmd_generate_keys_handler(
    public_key_file: Path,
    private_key_file: Path,
    key_size: int,
    min_prime_diff_bits: int,
    interactor: FromDishka[RSAGenerateKeysCommandHandler],
) -> None:
    """Generate RSA key pair and save to files."""
    if key_size <= 0:
        click.echo("Error: Key size must be positive", err=True)
        raise click.Abort()

    if key_size < 512:
        click.echo("Warning: Key size less than 512 bits is not recommended for security", err=True)

    if min_prime_diff_bits <= 0:
        click.echo("Error: Minimum prime difference bits must be positive", err=True)
        raise click.Abort()

    command: RSAGenerateKeysCommand = RSAGenerateKeysCommand(
        public_key_file=public_key_file,
        private_key_file=private_key_file,
        key_size=key_size,
        min_prime_diff_bits=min_prime_diff_bits,
    )

    try:
        view: RSAKeyGenerationView = asyncio.run(interactor(command))

        # Форматируем большие числа для читаемости
        def format_large_number(num: int, max_digits: int = 15) -> str:
            """Форматирует большое число, показывая начало и конец."""
            num_str = str(num)
            if len(num_str) <= max_digits * 2 + 3:
                return num_str
            return f"{num_str[:max_digits]}...{num_str[-max_digits:]}"

        table: PrettyTable = PrettyTable()
        table.title = "RSA Key Generation Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"  # left alignment
        table.max_width = 120
        
        table.add_row(["Key Size", f"{view.key_size} bits"])
        table.add_row([
            "Public Key (e)",
            f"{format_large_number(view.public_key_e)} ({view.public_key_e.bit_length()} bits)"
        ])
        table.add_row([
            "Public Key (n)",
            f"{format_large_number(view.public_key_n)} ({view.public_key_n.bit_length()} bits)"
        ])
        table.add_row([
            "Private Key (d)",
            f"{format_large_number(view.private_key_d)} ({view.private_key_d.bit_length()} bits)"
        ])
        table.add_row(["Public Key File", str(view.public_key_file)])
        table.add_row(["Private Key File", str(view.private_key_file)])

        click.echo(table)
        click.echo(f"\n✓ Keys generated and saved successfully!")
        click.echo(f"\nFull key values are saved to the files above.")

    except Exception as e:
        click.echo(f"Error during key generation: {e}", err=True)
        raise click.Abort() from e


@rsa_group.command("encrypt")
@click.option(
    "-m",
    "--message",
    required=True,
    help="Message to encrypt",
    type=str,
)
@click.option(
    "-k",
    "--public-key-file",
    required=True,
    help="Path to public key file",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-o",
    "--output-file",
    required=True,
    help="Path to save encrypted data",
    type=click.Path(path_type=Path),
)
def cmd_encrypt_handler(
    message: str,
    public_key_file: Path,
    output_file: Path,
    interactor: FromDishka[RSAEncryptCommandHandler],
) -> None:
    """Encrypt a message using RSA algorithm."""
    if not message or message.isspace():
        click.echo("Error: Message cannot be empty", err=True)
        return

    command: RSAEncryptCommand = RSAEncryptCommand(
        message=message.strip(),
        public_key_file=public_key_file,
        output_file=output_file,
    )

    try:
        view: RSAEncryptionView = asyncio.run(interactor(command))

        # Форматируем большие числа для читаемости
        def format_large_number(num: int, max_digits: int = 15) -> str:
            """Форматирует большое число, показывая начало и конец."""
            num_str = str(num)
            if len(num_str) <= max_digits * 2 + 3:
                return num_str
            return f"{num_str[:max_digits]}...{num_str[-max_digits:]}"

        table: PrettyTable = PrettyTable()
        table.title = "RSA Encryption Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Original Message", view.message])
        table.add_row([
            "Public Key (e)",
            f"{format_large_number(view.public_key_e)} ({view.public_key_e.bit_length()} bits)"
        ])
        table.add_row([
            "Public Key (n)",
            f"{format_large_number(view.public_key_n)} ({view.public_key_n.bit_length()} bits)"
        ])
        table.add_row(["Encrypted Blocks Count", str(len(view.encrypted_blocks))])
        table.add_row(["Output File", str(output_file)])

        click.echo(table)
        click.echo(f"\n✓ Encrypted data saved to: {output_file}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
    except Exception as e:
        click.echo(f"Error during encryption: {e}", err=True)
        raise click.Abort() from e


@rsa_group.command("decrypt")
@click.option(
    "-k",
    "--private-key-file",
    required=True,
    help="Path to private key file",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-i",
    "--encrypted-data-file",
    required=True,
    help="Path to file with encrypted data",
    type=click.Path(exists=True, path_type=Path),
)
def cmd_decrypt_handler(
    private_key_file: Path,
    encrypted_data_file: Path,
    interactor: FromDishka[RSADecryptCommandHandler],
) -> None:
    """Decrypt a message from file using RSA algorithm."""
    command: RSADecryptCommand = RSADecryptCommand(
        private_key_file=private_key_file,
        encrypted_data_file=encrypted_data_file,
    )

    try:
        view: RSADecryptionView = asyncio.run(interactor(command))

        table: PrettyTable = PrettyTable()
        table.title = "RSA Decryption Result"
        table.field_names = [
            "Parameter",
            "Value",
        ]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Decrypted Message", view.decrypted_message])
        table.add_row(["Encrypted Blocks Count", str(len(view.encrypted_blocks))])
        table.add_row(["Private Key File", str(private_key_file)])
        table.add_row(["Encrypted Data File", str(encrypted_data_file)])

        click.echo(table)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
    except ValueError as e:
        click.echo(f"Error: Invalid file format - {e}", err=True)
        raise click.Abort() from e
    except Exception as e:
        click.echo(f"Error during decryption: {e}", err=True)
        raise click.Abort() from e

