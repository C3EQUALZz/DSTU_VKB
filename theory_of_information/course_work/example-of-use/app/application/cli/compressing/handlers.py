from pathlib import Path

import click
from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.compression import (
    CompressFileCommand,
    DecompressFileCommand,
)
from app.logic.container import container
from app.logic.message_bus import MessageBus
from dishka import FromDishka
from dishka.integrations.click import setup_dishka


@click.group()
@click.pass_context
def cli(context: click.Context):
    BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)
    setup_dishka(container=container, context=context, auto_inject=True)


@cli.command("compress")
@click.argument("src_file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option(
    "-t",
    "--type_of_compression",
    type=click.Choice(["gzip", "pigz"]),
    default="gzip",
    help="Compression type",
)
def compress(
    src_file_path: Path, type_of_compression: str, bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    Compress any file that user gives
    :param src_file_path: path to file to compress
    :param type_of_compression: compression type
    :param bootstrap: Bootstrap
    :return: Returns nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(CompressFileCommand(src_file_path, compress_type=type_of_compression))
    click.echo("Compress complete.")


@cli.command("decompress")
@click.argument("src_file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option(
    "-t",
    "--type_of_compression",
    type=click.Choice(["gzip"]),
    default="gzip",
    help="Compression type",
)
def decompress(
    src_file_path: Path, type_of_compression: str, bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    Decompress any file that user gives
    :param src_file_path: File to decompress
    :param type_of_compression: Type of compression
    :param bootstrap: Bootstrap
    :return: Nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(DecompressFileCommand(src_file_path, compress_type=type_of_compression))
    click.echo("Decompress complete.")


if __name__ == "__main__":
    cli()
