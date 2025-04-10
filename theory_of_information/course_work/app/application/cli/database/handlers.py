from typing import TYPE_CHECKING

import click
from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.database import (CreateDatabaseBackupCommand,
                                         ListAllDatabasesCommand)
from app.logic.container import container
from app.settings.logger.config import setup_logging
from dishka import FromDishka
from dishka.integrations.click import setup_dishka

if TYPE_CHECKING:
    from app.logic.message_bus import MessageBus


@click.group()
@click.pass_context
def cli(context: click.Context):
    setup_logging()
    BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)
    setup_dishka(container=container, context=context, auto_inject=True)


@cli.command("list")
def list_all_databases(bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]) -> None:
    """
    Command to list all databases.
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(ListAllDatabasesCommand())
    click.echo("Successfully listed all databases")


@cli.command("backup")
@click.argument("database_name", type=click.STRING, required=True)
def backup_database(database_name: str, bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]) -> None:
    """
    Command to back up a database.
    :param database_name: name of the existing database
    :param bootstrap: bootstrap instance
    :return: nothing
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(CreateDatabaseBackupCommand(database_name=database_name))
    click.echo(f"Successfully backup the database {database_name}")


if __name__ == "__main__":
    cli()
