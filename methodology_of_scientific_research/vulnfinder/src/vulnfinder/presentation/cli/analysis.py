import logging
from pathlib import Path

import click
from dishka.integrations.click import FromDishka

from vulnfinder.application.commands.analysis import (
    AnalyzeCodeCommand,
    AnalyzeCodeCommandHandler,
)
from vulnfinder.application.queries.analysis import (
    CollectFilesQuery,
    CollectFilesQueryHandler,
    ParseExtensionsQuery,
    ParseExtensionsQueryHandler,
    ReadTextQuery,
    ReadTextQueryHandler,
)

logger = logging.getLogger(__name__)


@click.group(name="analysis")
def analysis_group() -> None:
    """Commands related to code analysis."""


@analysis_group.command("analyze")
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--context-query", type=str, default=None)
@click.option("--top-k", type=int, default=5, show_default=True)
@click.option("--recursive", is_flag=True, default=False, show_default=True)
@click.option(
    "--extensions",
    type=str,
    default=".py,.c,.cpp,.java",
    show_default=True,
    help="Comma-separated extensions for directory scan.",
)
def analyze_command(  # noqa: PLR0913
    path: Path,
    context_query: str | None,
    top_k: int,
    *,
    interactor: FromDishka[AnalyzeCodeCommandHandler],
    parse_extensions: FromDishka[ParseExtensionsQueryHandler],
    collect_files: FromDishka[CollectFilesQueryHandler],
    read_text: FromDishka[ReadTextQueryHandler],
    recursive: bool | None = None,
    extensions: str = ".py,.c,.cpp,.java",
) -> None:
    parsed_extensions = parse_extensions(
        ParseExtensionsQuery(extensions=extensions),
    )
    files = collect_files(
        CollectFilesQuery(
            path=path,
            recursive=recursive,
            extensions=parsed_extensions,
        ),
    )
    if not files:
        logger.warning("No files found for analysis.")
        return

    for file_path in files:
        code = read_text(ReadTextQuery(path=file_path))
        logger.info("Analyzing file: %s", file_path)
        result = interactor(
            AnalyzeCodeCommand(
                code=code,
                context_query=context_query,
                top_k=top_k,
                source_path=file_path,
                recursive=bool(recursive),
            ),
        )
        click.echo(f"\n# {file_path}\n")
        click.echo(result.raw_response)
