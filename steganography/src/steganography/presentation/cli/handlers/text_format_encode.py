"""click-команды для работы «Встраивание сокрытия в docx»."""

import asyncio
from pathlib import Path

import click
from dishka import FromDishka

from steganography.application.commands.text_format_encode.encode import (
    EncodeSecretCommand,
    EncodeSecretCommandHandler,
)
from steganography.application.common.views.text_format_encode import (
    EncodeSecretView,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.ports.cover_text_reader import (
    CoverTextReader,
)
from steganography.domain.text_format_encode.services.hiding_value_defaults import (
    HidingValueDefaults,
)
from steganography.presentation.cli.presenters.encode_result_presenter import (
    EncodeResultPresenter,
)

_ENCODING_CHOICES = ("МТК-2 (Бодо)", "КОИ-8R", "cp866", "Windows-1251", "ASCII")
_PARAM_CHOICES = tuple(param.value for param in FormattingParam)


@click.group(name="text-format-encode")
def text_format_encode_group() -> None:
    """Встраивание скрытых сообщений в docx-контейнеры."""


@text_format_encode_group.command("encode")
@click.option("-s", "--secret", required=True, help="Секретное сообщение.")
@click.option(
    "--cover-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="docx-контейнер с текстом (стихом и т.п.).",
)
@click.option(
    "--cover-text",
    default=None,
    help="Текст-контейнер напрямую (альтернатива --cover-file).",
)
@click.option(
    "-e", "--encoding",
    "encoding_name",
    type=click.Choice(_ENCODING_CHOICES),
    default="Windows-1251",
    show_default=True,
    help="Кодировка секретного сообщения.",
)
@click.option(
    "-p", "--param",
    type=click.Choice(_PARAM_CHOICES),
    default=FormattingParam.SIZE.value,
    show_default=True,
    help="Параметр форматирования для сокрытия.",
)
@click.option("--zero", "zero_value", default=None, help="Значение для бита 0.")
@click.option("--one", "one_value", default=None, help="Значение для бита 1.")
@click.option(
    "-o", "--output",
    "output_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Куда сохранить контейнер с сокрытием.",
)
def cmd_encode(  # noqa: PLR0913
    secret: str,
    cover_file: Path | None,
    cover_text: str | None,
    encoding_name: str,
    param: str,
    zero_value: str | None,
    one_value: str | None,
    output_path: Path,
    interactor: FromDishka[EncodeSecretCommandHandler],
    cover_reader: FromDishka[CoverTextReader],
    defaults: FromDishka[HidingValueDefaults],
    presenter: FromDishka[EncodeResultPresenter],
) -> None:
    """Встроить сообщение в контейнер и сохранить новый docx."""
    resolved_cover = _resolve_cover(cover_file, cover_text, cover_reader)
    if resolved_cover is None:
        click.echo("укажите --cover-file или --cover-text")
        return

    formatting_param = FormattingParam(param)
    default_zero, default_one = defaults.for_param(formatting_param)
    command = EncodeSecretCommand(
        secret_text=secret,
        cover_text=resolved_cover,
        encoding_name=encoding_name,
        param=formatting_param,
        zero_value=zero_value or default_zero,
        one_value=one_value or default_one,
        output_path=output_path,
    )
    view: EncodeSecretView = asyncio.run(interactor(command))
    click.echo(presenter.render(view))


def _resolve_cover(
    cover_file: Path | None,
    cover_text: str | None,
    cover_reader: CoverTextReader,
) -> str | None:
    if cover_text is not None:
        return cover_text.replace("\n", " ")
    if cover_file is not None:
        return cover_reader.read(cover_file)
    return None
