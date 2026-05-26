"""click-команды для работы «Декодирование форматирования в docx»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.application.common.views.text_format_decode import (
    DetectSecretView,
)
from steganography.presentation.cli.presenters.detect_result_presenter import (
    DetectResultPresenter,
)
from steganography.presentation.cli.presenters.detect_summary_presenter import (
    DetectSummaryPresenter,
)


@click.group(name="text-format-decode")
def text_format_decode_group() -> None:
    """Декодирование скрытых сообщений в docx-контейнерах."""


@text_format_decode_group.command("detect")
@click.option(
    "-f", "--file",
    "docx",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Путь к docx-файлу-контейнеру.",
)
def cmd_detect(
    docx: Path,
    interactor: FromDishka[DetectSecretCommandHandler],
    presenter: FromDishka[DetectResultPresenter],
) -> None:
    """Найти и расшифровать сообщение в одном файле."""
    view: DetectSecretView = asyncio.run(
        interactor(DetectSecretCommand(docx_path=docx)),
    )
    click.echo(presenter.render(view))


@text_format_decode_group.command("detect-all")
@click.option(
    "-d", "--directory",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Каталог с docx-контейнерами для пакетного анализа.",
)
@click.option(
    "--glob",
    "pattern",
    default="*.docx",
    show_default=True,
    help="Шаблон поиска docx-файлов.",
)
def cmd_detect_all(
    directory: Path,
    pattern: str,
    interactor: FromDishka[DetectSecretCommandHandler],
    presenter: FromDishka[DetectSummaryPresenter],
) -> None:
    """Прогнать детектор на всех docx в каталоге и вывести сводку."""
    files: list[Path] = sorted(directory.glob(pattern))
    if not files:
        click.echo(f"в каталоге {directory} нет файлов по шаблону {pattern}")
        return
    views: list[DetectSecretView] = [
        asyncio.run(interactor(DetectSecretCommand(docx_path=path)))
        for path in files
    ]
    click.echo(presenter.render(views))
