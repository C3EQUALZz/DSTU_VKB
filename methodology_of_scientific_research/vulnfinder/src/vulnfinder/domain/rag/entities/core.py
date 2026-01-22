from dataclasses import dataclass, field

from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity
from vulnfinder.domain.knowledge_base.value_objects.identifiers import KnowledgeEntryId
from vulnfinder.domain.rag.value_objects.identifiers import (
    ContextBundleId,
    RetrievedDocumentId,
)
from vulnfinder.domain.rag.value_objects.types import QueryEmbedding, SimilarityScore


@dataclass(eq=False, kw_only=True)
class RetrievedDocument(BaseEntity[RetrievedDocumentId]):
    content: str
    score: SimilarityScore
    source_entry_id: KnowledgeEntryId | None = None


@dataclass(eq=False, kw_only=True)
class ContextBundle(BaseAggregateRoot[ContextBundleId]):
    query: str
    documents: list[RetrievedDocument] = field(default_factory=list)
    embedding: QueryEmbedding | None = None

    def add_document(self, document: RetrievedDocument) -> None:
        self.documents.append(document)
