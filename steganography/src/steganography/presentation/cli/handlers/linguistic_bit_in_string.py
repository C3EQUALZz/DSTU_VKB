"""click-команды для работы «Лингвистическое сокрытие 1 бита в строке»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.linguistic_bit_in_string.classify import (
    ClassifyStringsCommand,
    ClassifyStringsCommandHandler,
)
from steganography.application.common.views.linguistic_bit_in_string import (
    ClassifyStringsView,
)
from steganography.presentation.cli.presenters.classification_result_presenter import (
    ClassificationResultPresenter,
)


@click.group(name="linguistic-bit-in-string")
def linguistic_bit_in_string_group() -> None:
    """Лингвистическая стеганография — сокрытие 1 бита в строке."""


@linguistic_bit_in_string_group.command("classify")
@click.option(
    "-i", "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Файл со строками (по одной на строку).",
)
@click.option(
    "-o", "--output",
    "output_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Файл для записи результатов классификации.",
)
def cmd_classify(
    input_path: Path,
    output_path: Path,
    interactor: FromDishka[ClassifyStringsCommandHandler],
    presenter: FromDishka[ClassificationResultPresenter],
) -> None:
    """Прочитать строки из файла и классифицировать каждую как «ДА» или «НЕТ»."""
    view: ClassifyStringsView = asyncio.run(
        interactor(
            ClassifyStringsCommand(
                input_path=input_path,
                output_path=output_path,
            ),
        ),
    )
    click.echo(presenter.render(view))
