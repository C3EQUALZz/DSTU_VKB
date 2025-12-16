"""CLI handlers for RSA digital signature operations."""
import asyncio
from pathlib import Path

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.rsa_signature.generate_keys import (
    RSASignatureGenerateKeysCommand,
    RSASignatureGenerateKeysCommandHandler,
)
from cryptography_methods.application.commands.rsa_signature.sign import (
    RSASignatureSignCommand,
    RSASignatureSignCommandHandler,
)
from cryptography_methods.application.commands.rsa_signature.verify import (
    RSASignatureVerifyCommand,
    RSASignatureVerifyCommandHandler,
)
from cryptography_methods.application.common.views.rsa_signature import (
    RSASignatureKeyGenerationView,
    RSASignatureSignView,
    RSASignatureVerifyView,
)


@click.group(name="rsa-sign")
def rsa_sign_group() -> None:
    """RSA-based digital signature commands."""
    ...


@rsa_sign_group.command("generate-keys")
@click.option(
    "-p",
    "--public-key-file",
    required=True,
    help="Path to save RSA signature public key (e, n)",
    type=click.Path(path_type=Path),
)
@click.option(
    "-pr",
    "--private-key-file",
    required=True,
    help="Path to save RSA signature private key (d, n)",
    type=click.Path(path_type=Path),
)
@click.option(
    "-s",
    "--key-size",
    default=2048,
    help="RSA key size in bits (default: 2048)",
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
    interactor: FromDishka[RSASignatureGenerateKeysCommandHandler],
) -> None:
    """Generate RSA keys for digital signatures."""
    if key_size <= 0:
        click.echo("Error: key-size must be positive", err=True)
        raise click.Abort()

    if min_prime_diff_bits <= 0:
        click.echo("Error: min-prime-diff-bits must be positive", err=True)
        raise click.Abort()

    command = RSASignatureGenerateKeysCommand(
        public_key_file=public_key_file,
        private_key_file=private_key_file,
        key_size=key_size,
        min_prime_diff_bits=min_prime_diff_bits,
    )

    try:
        view: RSASignatureKeyGenerationView = asyncio.run(interactor(command))

        table = PrettyTable()
        table.title = "RSA Signature Key Generation Result"
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Key Size", f"{view.key_size} bits"])
        table.add_row(["Min prime diff (bits)", str(view.min_prime_diff_bits)])
        table.add_row(["Modulus n (bits)", str(view.n_bits)])
        table.add_row(["Public Key File", view.public_key_file])
        table.add_row(["Private Key File", view.private_key_file])

        click.echo(table)
        click.echo("\n✓ RSA signature keys generated and saved successfully!")

    except Exception as exc:
        click.echo(f"Error during RSA signature key generation: {exc}", err=True)
        raise click.Abort() from exc


@rsa_sign_group.command("sign")
@click.option(
    "-d",
    "--document",
    required=True,
    help="Path to document to sign",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-k",
    "--private-key-file",
    required=True,
    help="Path to RSA signature private key file (d, n)",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-s",
    "--signature-file",
    help="Path to save signature (base64). Default: <document>.sig",
    type=click.Path(path_type=Path),
)
@click.option(
    "-h",
    "--hash-file",
    help="Path to save hash (hex). Default: <document>.sha256.txt",
    type=click.Path(path_type=Path),
)
def cmd_sign_handler(
    document: Path,
    private_key_file: Path,
    signature_file: Path | None,
    hash_file: Path | None,
    interactor: FromDishka[RSASignatureSignCommandHandler],
) -> None:
    """Sign a document with RSA digital signature."""
    signature_path = signature_file or document.with_suffix(document.suffix + ".sig")

    command = RSASignatureSignCommand(
        document_path=document,
        private_key_file=private_key_file,
        signature_file=signature_path,
        hash_file=hash_file,
    )

    try:
        view: RSASignatureSignView = asyncio.run(interactor(command))

        table = PrettyTable()
        table.title = "RSA Signature Creation Result"
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Document", view.document_path])
        table.add_row(["Hash (SHA-256, hex)", view.hash_hex])
        table.add_row(["Hash File", view.hash_file])
        table.add_row(["Signature File", view.signature_file])
        table.add_row(["Private Key File", view.key_file])

        click.echo(table)
        click.echo("\n✓ Document signed successfully.")

    except Exception as exc:
        click.echo(f"Error during RSA signature creation: {exc}", err=True)
        raise click.Abort() from exc


@rsa_sign_group.command("verify")
@click.option(
    "-d",
    "--document",
    required=True,
    help="Path to document to verify",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-s",
    "--signature-file",
    required=True,
    help="Path to signature file (base64)",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-k",
    "--public-key-file",
    required=True,
    help="Path to RSA signature public key file (e, n)",
    type=click.Path(exists=True, path_type=Path),
)
def cmd_verify_handler(
    document: Path,
    signature_file: Path,
    public_key_file: Path,
    interactor: FromDishka[RSASignatureVerifyCommandHandler],
) -> None:
    """Verify RSA digital signature for a document."""
    command = RSASignatureVerifyCommand(
        document_path=document,
        signature_file=signature_file,
        public_key_file=public_key_file,
    )

    try:
        view: RSASignatureVerifyView = asyncio.run(interactor(command))

        table = PrettyTable()
        table.title = "RSA Signature Verification Result"
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.max_width = 120

        table.add_row(["Document", view.document_path])
        table.add_row(["Signature File", view.signature_file])
        table.add_row(["Public Key File", view.key_file])
        table.add_row(["Document Hash (SHA-256, hex)", view.hash_hex])
        table.add_row(["Verification Result", "VALID" if view.is_valid else "INVALID"])

        click.echo(table)

    except Exception as exc:
        click.echo(f"Error during RSA signature verification: {exc}", err=True)
        raise click.Abort() from exc


@rsa_sign_group.command("compare-hashes")
@click.option(
    "-h1",
    "--hash-file-1",
    required=True,
    help="Path to first hash file (hex)",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-h2",
    "--hash-file-2",
    required=True,
    help="Path to second hash file (hex)",
    type=click.Path(exists=True, path_type=Path),
)
def cmd_compare_hashes_handler(hash_file_1: Path, hash_file_2: Path) -> None:
    """Compare two SHA-256 hashes stored in text files."""
    h1 = hash_file_1.read_text(encoding="utf-8").strip()
    h2 = hash_file_2.read_text(encoding="utf-8").strip()

    click.echo("\n=== Hash Comparison (SHA-256) ===")
    click.echo(f"Hash 1 ({len(h1)} chars):\n{h1}")
    click.echo(f"\nHash 2 ({len(h2)} chars):\n{h2}")

    equal = h1 == h2
    click.echo(f"\nResult: hashes {'MATCH' if equal else 'DO NOT MATCH'}")

    if not equal:
        click.echo("\nDifferences by position:")
        max_len = max(len(h1), len(h2))
        for i in range(max_len):
            c1 = h1[i] if i < len(h1) else " "
            c2 = h2[i] if i < len(h2) else " "
            if c1 != c2:
                click.echo(f"Position {i + 1}: '{c1}' vs '{c2}'")


@rsa_sign_group.command("compare-signatures")
@click.option(
    "-s1",
    "--signature-file-1",
    required=True,
    help="Path to first signature file (base64)",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-s2",
    "--signature-file-2",
    required=True,
    help="Path to second signature file (base64)",
    type=click.Path(exists=True, path_type=Path),
)
def cmd_compare_signatures_handler(signature_file_1: Path, signature_file_2: Path) -> None:
    """Compare two RSA signatures (byte-by-byte)."""
    import base64

    s1_b64 = signature_file_1.read_text(encoding="utf-8").strip()
    s2_b64 = signature_file_2.read_text(encoding="utf-8").strip()

    try:
        sig1 = base64.b64decode(s1_b64, validate=True)
        sig2 = base64.b64decode(s2_b64, validate=True)
    except Exception as exc:
        click.echo(f"Error decoding signature files as base64: {exc}", err=True)
        raise click.Abort() from exc

    click.echo("\n=== Signature Comparison ===")
    click.echo(f"Signature 1 length: {len(sig1)} bytes")
    click.echo(f"Signature 2 length: {len(sig2)} bytes")
    click.echo(f"\nSignature 1 (hex):\n{sig1.hex()}")
    click.echo(f"\nSignature 2 (hex):\n{sig2.hex()}")

    equal = sig1 == sig2
    click.echo(f"\nResult: signatures {'MATCH' if equal else 'DO NOT MATCH'}")

    if not equal:
        click.echo("\nByte-level differences:")
        max_len = max(len(sig1), len(sig2))
        for i in range(max_len):
            b1 = sig1[i] if i < len(sig1) else 0
            b2 = sig2[i] if i < len(sig2) else 0
            if b1 != b2:
                click.echo(f"Byte {i + 1}: 0x{b1:02X} vs 0x{b2:02X}")


