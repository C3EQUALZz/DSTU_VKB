"""Точка входа CLI: ``python -m steganography.cli ...``."""

import click
from dishka import Container, make_container
from dishka.integrations.click import setup_dishka

from steganography.setup.bootstrap import setup_cli_routes, setup_logging
from steganography.setup.ioc_cli import setup_providers
from steganography.setup.settings import build_logging_config


@click.group()
@click.pass_context
def main(context: click.Context) -> None:
    """CLI к лабораторным курса «Стеганография»."""
    setup_logging(build_logging_config())

    container: Container = make_container(*setup_providers())
    setup_dishka(container, context=context, auto_inject=True)


def cli_entry() -> None:
    """Entry-point для console_scripts: собирает маршруты и запускает CLI."""
    setup_cli_routes(main)
    main()


if __name__ == "__main__":
    cli_entry()
