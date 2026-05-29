"""click-команды для КДБ8 «Метод Куттера-Джордана-Боссена»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.kutter_jordan_bossen.embed import (
    EmbedKjbCommand,
    EmbedKjbCommandHandler,
)
from steganography.application.commands.kutter_jordan_bossen.extract import (
    ExtractKjbCommand,
    ExtractKjbCommandHandler,
)
from steganography.application.common.views.kutter_jordan_bossen import (
    EmbedKjbView,
    ExtractKjbView,
)
from steganography.presentation.cli.presenters.embed_kjb_presenter import (
    EmbedKjbPresenter,
)
from steganography.presentation.cli.presenters.extract_kjb_presenter import (
    ExtractKjbPresenter,
)


@click.group(name="kutter-jordan-bossen")
def kutter_jordan_bossen_group() -> None:
    """Стеганография в синей компоненте RGB методом Куттера-Джордана-Боссена."""


@kutter_jordan_bossen_group.command("embed")
@click.option("-s", "--secret", required=True, help="Текст сообщения.")
@click.option(
    "-l", "--lambda-factor",
    "lambda_factor",
    type=float,
    default=0.1,
    show_default=True,
    help="Сила встраивания (доля от яркости).",
)
@click.option(
    "--seed",
    type=int,
    default=42,
    show_default=True,
    help="Seed PRNG выбора пикселей-носителей.",
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
    lambda_factor: float,
    seed: int,
    cover_path: Path,
    output_path: Path,
    interactor: FromDishka[EmbedKjbCommandHandler],
    presenter: FromDishka[EmbedKjbPresenter],
) -> None:
    """Встроить сообщение в синий канал BMP методом КДБ."""
    view: EmbedKjbView = asyncio.run(
        interactor(
            EmbedKjbCommand(
                cover_path=cover_path,
                output_path=output_path,
                secret_text=secret,
                lambda_factor=lambda_factor,
                seed=seed,
            ),
        ),
    )
    click.echo(presenter.render(view))


@kutter_jordan_bossen_group.command("extract")
@click.option(
    "-l", "--lambda-factor",
    "lambda_factor",
    type=float,
    default=0.1,
    show_default=True,
    help="Тот же параметр λ, что и при встраивании.",
)
@click.option(
    "--seed",
    type=int,
    default=42,
    show_default=True,
    help="Тот же seed, что и при встраивании.",
)
@click.option(
    "-c", "--container",
    "container_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="BMP-контейнер со скрытым сообщением.",
)
def cmd_extract(
    lambda_factor: float,
    seed: int,
    container_path: Path,
    interactor: FromDishka[ExtractKjbCommandHandler],
    presenter: FromDishka[ExtractKjbPresenter],
) -> None:
    """Извлечь сообщение из BMP, используя тот же seed."""
    view: ExtractKjbView = asyncio.run(
        interactor(
            ExtractKjbCommand(
                container_path=container_path,
                lambda_factor=lambda_factor,
                seed=seed,
            ),
        ),
    )
    click.echo(presenter.render(view))
