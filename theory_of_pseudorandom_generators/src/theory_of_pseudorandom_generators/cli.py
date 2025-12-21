import os

import click
from dishka import Container, make_container
from dishka.integrations.click import setup_dishka

from theory_of_pseudorandom_generators.setup.bootstrap import setup_cli_routes, setup_logging
from theory_of_pseudorandom_generators.setup.config_logger import LoggingConfig
from theory_of_pseudorandom_generators.setup.ioc import setup_providers


@click.group()
@click.pass_context
def main(context: click.Context) -> None:
    setup_logging(LoggingConfig(**os.environ))

    container: Container = make_container(
        *setup_providers(),
    )

    setup_dishka(container, context=context, auto_inject=True)


if __name__ == "__main__":
    setup_cli_routes(main)
    main()


