"""click-команды для ПР6 «LSB в BMP с шифрованием Виженера»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.lsb_bmp_vigenere.embed import (
    EmbedLsbBmpCommand,
    EmbedLsbBmpCommandHandler,
)
from steganography.application.commands.lsb_bmp_vigenere.extract import (
    ExtractLsbBmpCommand,
    ExtractLsbBmpCommandHandler,
)
from steganography.application.common.views.lsb_bmp_vigenere import (
    EmbedLsbBmpView,
    ExtractLsbBmpView,
)
from steganography.presentation.cli.presenters.embed_lsb_bmp_presenter import (
    EmbedLsbBmpPresenter,
)
from steganography.presentation.cli.presenters.extract_lsb_bmp_presenter import (
    ExtractLsbBmpPresenter,
)


@click.group(name="lsb-bmp-vigenere")
def lsb_bmp_vigenere_group() -> None:
    """LSB-стеганография в BMP с шифрованием Виженера и метками."""


@lsb_bmp_vigenere_group.command("embed")
@click.option("-s", "--secret", required=True, help="Открытое сообщение.")
@click.option("-k", "--key", required=True, help="Ключ шифра Виженера.")
@click.option(
    "-c", "--cover",
    "cover_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="BMP-контейнер.",
)
@click.option(
    "-o", "--output",
    "output_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Файл-результат BMP.",
)
def cmd_embed(  # noqa: PLR0913
    secret: str,
    key: str,
    cover_path: Path,
    output_path: Path,
    interactor: FromDishka[EmbedLsbBmpCommandHandler],
    presenter: FromDishka[EmbedLsbBmpPresenter],
) -> None:
    """Зашифровать сообщение, обернуть метками и встроить в LSB BMP."""
    view: EmbedLsbBmpView = asyncio.run(
        interactor(
            EmbedLsbBmpCommand(
                cover_path=cover_path,
                output_path=output_path,
                secret_text=secret,
                key=key,
            ),
        ),
    )
    click.echo(presenter.render(view))


@lsb_bmp_vigenere_group.command("extract")
@click.option("-k", "--key", required=True, help="Ключ шифра Виженера.")
@click.option(
    "-c", "--container",
    "container_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="BMP-контейнер со встроенным сообщением.",
)
def cmd_extract(
    key: str,
    container_path: Path,
    interactor: FromDishka[ExtractLsbBmpCommandHandler],
    presenter: FromDishka[ExtractLsbBmpPresenter],
) -> None:
    """Извлечь и расшифровать сообщение из BMP-контейнера."""
    view: ExtractLsbBmpView = asyncio.run(
        interactor(
            ExtractLsbBmpCommand(
                container_path=container_path,
                key=key,
            ),
        ),
    )
    click.echo(presenter.render(view))
