import logging
from pathlib import Path

import click
from dishka.integrations.click import FromDishka

from vulnfinder.application.commands.analysis import AnalyzeCodeCommand, AnalyzeCodeCommandHandler

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
def analyze_command(
    path: Path,
    context_query: str | None,
    top_k: int,
    recursive: bool,
    extensions: str,
    interactor: FromDishka[AnalyzeCodeCommandHandler],
) -> None:
    files = _collect_files(path, recursive=recursive, extensions=_parse_extensions(extensions))
    if not files:
        logger.warning("No files found for analysis.")
        return

    for file_path in files:
        code = _read_text(file_path)
        logger.info("Analyzing file: %s", file_path)
        result = interactor(
            AnalyzeCodeCommand(
                code=code,
                context_query=context_query,
                top_k=top_k,
            ),
        )
        click.echo(f"\n# {file_path}\n")
        click.echo(result.raw_response)


def _parse_extensions(extensions: str) -> tuple[str, ...]:
    return tuple(ext.strip().lower() for ext in extensions.split(",") if ext.strip())


def _collect_files(path: Path, recursive: bool, extensions: tuple[str, ...]) -> list[Path]:
    if path.is_file():
        return [path]

    pattern = "**/*" if recursive else "*"
    results = [entry for entry in path.glob(pattern) if entry.is_file()]
    if extensions:
        results = [entry for entry in results if entry.suffix.lower() in extensions]
    return results


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

