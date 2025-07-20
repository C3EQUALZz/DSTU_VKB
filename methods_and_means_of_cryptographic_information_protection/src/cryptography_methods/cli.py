import click
from dishka import Container, make_container
from dishka.integrations.click import setup_dishka

from cryptography_methods.setup.bootstrap import setup_logging, setup_cli_routes
from cryptography_methods.setup.ioc_cli import setup_providers
from cryptography_methods.setup.settings import (
    LoggingConfig
)


@click.group()
@click.pass_context
def main(context: click.Context) -> None:
    setup_logging(LoggingConfig())

    container: Container = make_container(
        *setup_providers(),
    )

    setup_dishka(container, context=context, auto_inject=True)


if __name__ == "__main__":
    setup_cli_routes(main)
    main()
