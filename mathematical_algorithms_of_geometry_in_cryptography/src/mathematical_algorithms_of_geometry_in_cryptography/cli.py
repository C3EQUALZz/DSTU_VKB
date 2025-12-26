import click
from dishka import Container, make_container
from dishka.integrations.click import setup_dishka

from mathematical_algorithms_of_geometry_in_cryptography.setup.bootstrap import setup_logging, setup_cli_routes
from mathematical_algorithms_of_geometry_in_cryptography.setup.config_logger import (
    LoggingConfig
)
from mathematical_algorithms_of_geometry_in_cryptography.setup.ioc import setup_providers


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
