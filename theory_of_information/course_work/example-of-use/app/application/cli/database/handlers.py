import click
from dishka import FromDishka
from dishka.integrations.click import setup_dishka

from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.database import ListAllDatabasesCommand
from app.logic.container import container
from app.logic.message_bus import MessageBus


@click.group()
@click.pass_context
def cli(context: click.Context):
    setup_dishka(container=container, context=context, auto_inject=True)


@cli.command("list")
def list_all_databases(bootstrap: FromDishka[Bootstrap[CompressionUnitOfWork]]) -> None:
    """
    Command to list all databases.
    :return:
    """
    message_bus: MessageBus = bootstrap.get_messagebus()
    message_bus.handle(ListAllDatabasesCommand())
    click.echo("Successfully listed all databases")


if __name__ == '__main__':
    cli()
