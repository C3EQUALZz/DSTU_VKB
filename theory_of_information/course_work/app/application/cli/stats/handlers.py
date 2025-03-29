from pathlib import Path

import click
from dishka import FromDishka
from dishka.integrations.click import setup_dishka

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.stats import GetFileFullStatsCommand
from app.logic.container import container
from app.logic.message_bus import MessageBus
from app.settings.logger.config import setup_logging


@click.group()
@click.pass_context
def cli(context: click.Context):
    setup_logging()
    BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)
    setup_dishka(container=container, context=context, auto_inject=True)


@cli.command("stats")
@click.argument("src_file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
def get_file_stats(
        src_file_path: Path,
        bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]
) -> None:
    """
    Handler for getting info about statistics of file.
    :param src_file_path: file path in your system to file.
    :param bootstrap: Bootstrap instance
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(GetFileFullStatsCommand(file_path=src_file_path))
    click.echo("File stats complete.")

if __name__ == "__main__":
    cli()