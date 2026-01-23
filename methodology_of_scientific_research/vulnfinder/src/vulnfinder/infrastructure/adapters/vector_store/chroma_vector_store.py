from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from langchain_core.documents import Document
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)
from typing_extensions import override

from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway

if TYPE_CHECKING:
    from collections.abc import Sequence

    from langchain_core.vectorstores import VectorStore


class ChromaVectorStoreGateway(VectorStoreGateway):
    def __init__(self, vector_store: VectorStore) -> None:
        self._vector_store: Final[VectorStore] = vector_store

    @override
    def add_documents(self, documents: list[KnowledgeDocument]) -> None:
        langchain_docs = [
            Document(page_content=doc.content, metadata=dict(doc.metadata))
            for doc in documents
        ]
        if not langchain_docs:
            return

        self._add_in_batches(langchain_docs, batch_size=256)

    def _add_in_batches(self, docs: list[Document], batch_size: int) -> None:
        for start in range(0, len(docs), batch_size):
            chunk = docs[start : start + batch_size]
            try:
                self._add_with_retry(chunk)
            except ValueError as exc:
                if "No embedding data received" in str(exc) and len(chunk) > 1:
                    midpoint = max(1, len(chunk) // 2)
                    self._add_in_batches(chunk[:midpoint], max(1, batch_size // 2))
                    self._add_in_batches(chunk[midpoint:], max(1, batch_size // 2))
                else:
                    raise

    @retry(
        retry=retry_if_exception(lambda exc: "No embedding data received" in str(exc)),
        wait=wait_exponential_jitter(initial=0.5, max=5.0),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def _add_with_retry(self, chunk: list[Document]) -> None:
        self._vector_store.add_documents(chunk)

    @override
    def similarity_search(self, query: str, k: int) -> list[KnowledgeDocument]:
        results: Sequence[Document] = self._vector_store.similarity_search(query, k=k)
        return [
            KnowledgeDocument(
                content=doc.page_content,
                metadata=self._normalize_metadata(doc.metadata),
            )
            for doc in results
        ]

    @override
    def get_document_count(self) -> int:
        collection: Any = getattr(self._vector_store, "_collection", None)
        if collection is None:
            return 0
        return int(collection.count())

    @staticmethod
    def _normalize_metadata(metadata: dict[str, object]) -> dict[str, str]:
        return {key: str(value) for key, value in metadata.items()}
