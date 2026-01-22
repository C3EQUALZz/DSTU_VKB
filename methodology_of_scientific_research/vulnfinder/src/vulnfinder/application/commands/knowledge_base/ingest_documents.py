from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from vulnfinder.application.common.ports.knowledge_source import KnowledgeSource
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class IngestDocumentsCommand:
    source_path: Path


@final
class IngestDocumentsCommandHandler:
    def __init__(
        self,
        knowledge_source: KnowledgeSource,
        vector_store: VectorStoreGateway,
    ) -> None:
        self._knowledge_source: Final[KnowledgeSource] = knowledge_source
        self._vector_store: Final[VectorStoreGateway] = vector_store

    def __call__(self, data: IngestDocumentsCommand) -> int:
        documents = self._knowledge_source.load(data.source_path)
        self._vector_store.add_documents(documents)
        return len(documents)
