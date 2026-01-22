from pathlib import Path

import click
from dishka.integrations.click import FromDishka

from vulnfinder.application.commands.knowledge_base import (
    EnsureKnowledgeBaseCommand,
    EnsureKnowledgeBaseCommandHandler,
    IngestDocumentsCommand,
    IngestDocumentsCommandHandler,
)


@click.group(name="kb")
def knowledge_base_group() -> None:
    """Knowledge base commands."""


@knowledge_base_group.command("update")
@click.option("--force", is_flag=True, default=False, show_default=True)
def kb_update(
    force: bool,
    interactor: FromDishka[EnsureKnowledgeBaseCommandHandler],
) -> None:
    interactor(EnsureKnowledgeBaseCommand(force_refresh=force))


@knowledge_base_group.command("ingest")
@click.argument("source_path", type=click.Path(exists=True, path_type=str))
def kb_ingest(
    source_path: str,
    interactor: FromDishka[IngestDocumentsCommandHandler],
) -> None:
    command = IngestDocumentsCommand(source_path=Path(source_path))
    count = interactor(command)
    click.echo(f"Ingested {count} documents.")

