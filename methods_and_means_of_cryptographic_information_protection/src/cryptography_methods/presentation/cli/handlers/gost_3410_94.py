"""CLI handlers for GOST 3410-94 digital signature."""

import asyncio
import logging
from pathlib import Path
from typing import Final

import click
from dishka import FromDishka
from prettytable import PrettyTable

from cryptography_methods.application.commands.gost_3410_94.compare_hashes import (
    Gost341094CompareHashesCommand,
    Gost341094CompareHashesCommandHandler,
)
from cryptography_methods.application.commands.gost_3410_94.generate_keys import (
    Gost341094GenerateKeysCommand,
    Gost341094GenerateKeysCommandHandler,
)
from cryptography_methods.application.commands.gost_3410_94.sign import (
    Gost341094SignCommand,
    Gost341094SignCommandHandler,
)
from cryptography_methods.application.commands.gost_3410_94.verify import (
    Gost341094VerifyCommand,
    Gost341094VerifyCommandHandler,
)
logger: Final[logging.Logger] = logging.getLogger(__name__)


def format_large_number(value: str | int, max_length: int = 50) -> str:
    """Форматирует большое число для отображения в таблице.

    Args:
        value: Число (строка или int)
        max_length: Максимальная длина для отображения

    Returns:
        Отформатированная строка
    """
    value_str = str(value)
    if len(value_str) <= max_length:
        return value_str
    return f"{value_str[:max_length]}... ({len(value_str)} символов)"


@click.group(name="gost-3410-94")
def gost_3410_94_group() -> None:
    """ГОСТ Р 34.10-94 — Управление ЭЦП."""
    pass


@gost_3410_94_group.command("generate-keys")
@click.option(
    "-p",
    "--parameters-file",
    required=True,
    type=click.Path(path_type=Path),
    help="Путь к файлу параметров (p, q, a)",
)
@click.option(
    "-pr",
    "--private-key-file",
    required=True,
    type=click.Path(path_type=Path),
    help="Путь к файлу закрытого ключа (x)",
)
@click.option(
    "-pub",
    "--public-key-file",
    required=True,
    type=click.Path(path_type=Path),
    help="Путь к файлу открытого ключа (y)",
)
@click.option(
    "-s",
    "--key-size",
    default=512,
    type=click.IntRange(512, 1024),
    help="Размер ключа в битах (512 или 1024)",
)
def cmd_generate_keys_handler(
    parameters_file: Path,
    private_key_file: Path,
    public_key_file: Path,
    key_size: int,
    interactor: FromDishka[Gost341094GenerateKeysCommandHandler],
) -> None:
    """Генерация параметров и ключей ГОСТ Р 34.10-94."""
    command = Gost341094GenerateKeysCommand(
        parameters_file=parameters_file,
        private_key_file=private_key_file,
        public_key_file=public_key_file,
        key_size=key_size,
    )

    try:
        view = asyncio.run(interactor(command))

        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.add_row(["Key Size", f"{view.key_size} bits"])
        table.add_row(["Prime p (bits)", view.p_bits])
        table.add_row(["Prime q (bits)", view.q_bits])
        table.add_row(["Parameters File", view.parameters_file])
        table.add_row(["Private Key File", view.private_key_file])
        table.add_row(["Public Key File", view.public_key_file])

        print("\n" + "=" * 50)
        print("     GOST 3410-94 Key Generation Result")
        print("=" * 50)
        print(table)
        print("\n✓ GOST 3410-94 keys generated and saved successfully!")
    except Exception as e:
        logger.exception("Error during GOST 3410-94 key generation")
        raise click.ClickException(f"Error during GOST 3410-94 key generation: {e}") from e


@gost_3410_94_group.command("sign")
@click.option(
    "-d",
    "--document",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к документу для подписания",
)
@click.option(
    "-p",
    "--parameters-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу параметров",
)
@click.option(
    "-k",
    "--private-key-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу закрытого ключа",
)
@click.option(
    "-s",
    "--signature-file",
    type=click.Path(path_type=Path),
    help="Путь к файлу подписи (по умолчанию: <document>.txt)",
)
@click.option(
    "-h",
    "--hash-file",
    type=click.Path(path_type=Path),
    help="Путь к файлу хеша (по умолчанию: Хеш_<document>.txt)",
)
def cmd_sign_handler(
    document: Path,
    parameters_file: Path,
    private_key_file: Path,
    signature_file: Path | None,
    hash_file: Path | None,
    interactor: FromDishka[Gost341094SignCommandHandler],
) -> None:
    """Подписать документ по ГОСТ Р 34.10-94."""
    signature_path = signature_file or document.with_suffix(".txt")

    command = Gost341094SignCommand(
        document=document,
        parameters_file=parameters_file,
        private_key_file=private_key_file,
        signature_file=signature_path,
        hash_file=hash_file,
    )

    try:
        view = asyncio.run(interactor(command))

        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.add_row(["Document", view.document_path])
        table.add_row(["Hash", format_large_number(view.hash_value)])
        table.add_row(["Hash File", view.hash_file])
        table.add_row(["Signature r", format_large_number(view.r)])
        table.add_row(["Signature s", format_large_number(view.s)])
        table.add_row(["Signature File", view.signature_file])

        print("\n" + "=" * 50)
        print("      GOST 3410-94 Signature Result")
        print("=" * 50)
        print(table)
        print(f"\n✓ GOST 3410-94 signature saved to: {view.signature_file}")
    except Exception as e:
        logger.exception("Error during GOST 3410-94 signing")
        raise click.ClickException(f"Error during GOST 3410-94 signing: {e}") from e


@gost_3410_94_group.command("verify")
@click.option(
    "-d",
    "--document",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к документу для проверки",
)
@click.option(
    "-s",
    "--signature-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу подписи",
)
@click.option(
    "-p",
    "--parameters-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу параметров",
)
@click.option(
    "-k",
    "--public-key-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к файлу открытого ключа",
)
def cmd_verify_handler(
    document: Path,
    signature_file: Path,
    parameters_file: Path,
    public_key_file: Path,
    interactor: FromDishka[Gost341094VerifyCommandHandler],
) -> None:
    """Проверить подпись документа по ГОСТ Р 34.10-94."""
    command = Gost341094VerifyCommand(
        document=document,
        signature_file=signature_file,
        parameters_file=parameters_file,
        public_key_file=public_key_file,
    )

    try:
        view = asyncio.run(interactor(command))

        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.add_row(["Document", view.document_path])
        table.add_row(["Signature File", view.signature_file])
        table.add_row(["Hash", format_large_number(view.hash_value)])
        table.add_row(["Result", "VALID" if view.is_valid else "INVALID"])

        print("\n" + "=" * 50)
        print("    GOST 3410-94 Signature Verification")
        print("=" * 50)
        print(table)
        print(f"\n{'✓' if view.is_valid else '✗'} Signature is {'VALID' if view.is_valid else 'INVALID'}")
    except Exception as e:
        logger.exception("Error during GOST 3410-94 verification")
        raise click.ClickException(f"Error during GOST 3410-94 verification: {e}") from e


@gost_3410_94_group.command("compare-hashes")
@click.option(
    "-h1",
    "--hash-file-1",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь к первому файлу хеша",
)
@click.option(
    "-h2",
    "--hash-file-2",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Путь ко второму файлу хеша",
)
def cmd_compare_hashes_handler(
    hash_file_1: Path,
    hash_file_2: Path,
    interactor: FromDishka[Gost341094CompareHashesCommandHandler],
) -> None:
    """Сравнить хеши двух файлов."""
    command = Gost341094CompareHashesCommand(
        hash_file_1=hash_file_1,
        hash_file_2=hash_file_2,
    )

    try:
        view = asyncio.run(interactor(command))

        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]
        table.align = "l"
        table.add_row(["Hash File 1", view.hash_file_1])
        table.add_row(["Hash 1", format_large_number(view.hash_1)])
        table.add_row(["Hash File 2", view.hash_file_2])
        table.add_row(["Hash 2", format_large_number(view.hash_2)])
        table.add_row(["Result", "Хеши совпадают" if view.are_equal else "Хеши не совпадают"])

        print("\n" + "=" * 50)
        print("      GOST 3410-94 Hash Comparison")
        print("=" * 50)
        print(table)
    except Exception as e:
        logger.exception("Error during GOST 3410-94 hash comparison")
        raise click.ClickException(f"Error during GOST 3410-94 hash comparison: {e}") from e

