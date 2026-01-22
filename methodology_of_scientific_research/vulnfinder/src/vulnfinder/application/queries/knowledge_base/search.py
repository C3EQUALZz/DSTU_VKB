from dataclasses import dataclass
from typing import Final, final

from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchKnowledgeBaseQuery:
    query: str
    top_k: int = 5


@final
class SearchKnowledgeBaseQueryHandler:
    def __init__(self, vector_store: VectorStoreGateway) -> None:
        self._vector_store: Final[VectorStoreGateway] = vector_store

    def __call__(self, data: SearchKnowledgeBaseQuery) -> list[KnowledgeDocument]:
        return self._vector_store.similarity_search(data.query, data.top_k)
