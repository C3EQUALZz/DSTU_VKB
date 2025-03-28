import click
from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.logic.container import container
from dishka.integrations.click import setup_dishka


@click.group()
@click.pass_context
def cli(context: click.Context):
    BACKUP_DIRECTORY_PATH.mkdir(exist_ok=True)
    setup_dishka(container=container, context=context, auto_inject=True)
