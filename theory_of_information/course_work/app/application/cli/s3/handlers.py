from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID

import click
from dishka import FromDishka
from dishka.integrations.click import setup_dishka

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.s3 import (
    CreateFileInS3Command,
    GetFileFromS3Command,
    ListFilesInS3Command,
)
from app.logic.container import container
from app.settings.logger.config import setup_logging

if TYPE_CHECKING:
    from app.logic.message_bus import MessageBus


@click.group()
@click.pass_context
def cli(context: click.Context):
    setup_logging()
    BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)
    setup_dishka(container=container, context=context, auto_inject=True)


@cli.command("upload")
@click.argument(
    "src_file_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True
)
@click.option(
    "-d", "--delete",
    is_flag=True,
)
def upload_file_to_s3(
        src_file_path: Path,
        delete: bool,
        bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    Upload file to s3. Please compress file before uploading.
    :param src_file_path: path to file in local server.
    :param delete: Is file must be deleted on local server or not after uploading to s3.
    :param bootstrap: Bootstrap instance.
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(CreateFileInS3Command(file_path=src_file_path, delete=delete))
    click.echo(f"Downloaded to S3, result: {message_bus.command_result}")


@cli.command("download")
@click.argument(
    "oid",
    type=click.UUID,
    required=True
)
def download_file_from_s3(
        oid: UUID,
        bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    Download file from s3.
    :param oid: the unique identifier to get file from S3
    :param bootstrap: Bootstrap instance.
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(GetFileFromS3Command(oid=str(oid)))
    click.echo(f"Downloaded from S3, result: {message_bus.command_result}")


@cli.command("list")
@click.option(
    "-s", "--start",
    type=int,
    default=0,
    help="Start index from which file will be downloaded."
)
@click.option(
    "-e", "--end",
    type=int,
    default=10,
    help="End index from which file will be downloaded."
)
def list_all_file_in_bucket(
        start: int,
        end: int,
        bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    List all files in s3 bucket.
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(ListFilesInS3Command(start=start, end=end))
    click.echo(f"Success! Message bus result: {message_bus.command_result}")


if __name__ == "__main__":
    cli()
