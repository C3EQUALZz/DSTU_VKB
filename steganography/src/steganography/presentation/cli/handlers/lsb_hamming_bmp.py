"""click-команды для ПР7 «LSB-R / LSB-M / Хемминг в BMP»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.lsb_hamming_bmp.embed import (
    EmbedLsbHammingCommand,
    EmbedLsbHammingCommandHandler,
)
from steganography.application.commands.lsb_hamming_bmp.extract import (
    ExtractLsbHammingCommand,
    ExtractLsbHammingCommandHandler,
)
from steganography.application.common.views.lsb_hamming_bmp import (
    EmbedLsbHammingView,
    ExtractLsbHammingView,
)
from steganography.domain.lsb_hamming_bmp.value_objects.embedding_method import (
    EmbeddingMethod,
)
from steganography.presentation.cli.presenters.embed_lsb_hamming_presenter import (
    EmbedLsbHammingPresenter,
)
from steganography.presentation.cli.presenters.extract_lsb_hamming_presenter import (
    ExtractLsbHammingPresenter,
)

_METHOD_CHOICES = tuple(method.value for method in EmbeddingMethod)


@click.group(name="lsb-hamming-bmp")
def lsb_hamming_bmp_group() -> None:
    """Стеганография изображений: LSB-R / LSB-M / Хемминг (15,11)."""


@lsb_hamming_bmp_group.command("embed")
@click.option("-s", "--secret", required=True, help="Текст сообщения.")
@click.option(
    "-m", "--method",
    type=click.Choice(_METHOD_CHOICES),
    default=EmbeddingMethod.LSB_REPLACEMENT.value,
    show_default=True,
    help="Метод встраивания.",
)
@click.option(
    "--step",
    type=int,
    default=1,
    show_default=True,
    help="Шаг между каналами (для LSB-R/LSB-M; для Хемминг игнорируется).",
)
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
    method: str,
    step: int,
    cover_path: Path,
    output_path: Path,
    interactor: FromDishka[EmbedLsbHammingCommandHandler],
    presenter: FromDishka[EmbedLsbHammingPresenter],
) -> None:
    """Встроить сообщение выбранным методом."""
    view: EmbedLsbHammingView = asyncio.run(
        interactor(
            EmbedLsbHammingCommand(
                cover_path=cover_path,
                output_path=output_path,
                secret_text=secret,
                method=EmbeddingMethod(method),
                step=step,
            ),
        ),
    )
    click.echo(presenter.render(view))


@lsb_hamming_bmp_group.command("extract")
@click.option(
    "-m", "--method",
    type=click.Choice(_METHOD_CHOICES),
    default=EmbeddingMethod.LSB_REPLACEMENT.value,
    show_default=True,
    help="Метод, которым было встроено сообщение.",
)
@click.option(
    "--step",
    type=int,
    default=1,
    show_default=True,
    help="Шаг между каналами (для LSB-R/LSB-M; для Хемминг игнорируется).",
)
@click.option(
    "-c", "--container",
    "container_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="BMP-контейнер со встроенным сообщением.",
)
def cmd_extract(
    method: str,
    step: int,
    container_path: Path,
    interactor: FromDishka[ExtractLsbHammingCommandHandler],
    presenter: FromDishka[ExtractLsbHammingPresenter],
) -> None:
    """Извлечь сообщение тем же методом, которым оно было встроено."""
    view: ExtractLsbHammingView = asyncio.run(
        interactor(
            ExtractLsbHammingCommand(
                container_path=container_path,
                method=EmbeddingMethod(method),
                step=step,
            ),
        ),
    )
    click.echo(presenter.render(view))
