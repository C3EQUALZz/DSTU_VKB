from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService
from vulnfinder.domain.rag.entities.core import ContextBundle, RetrievedDocument
from vulnfinder.domain.rag.value_objects.identifiers import (
    ContextBundleId,
    RetrievedDocumentId,
)
from vulnfinder.domain.rag.value_objects.types import QueryEmbedding, SimilarityScore


class RagFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider = uuid_provider

    def create_bundle(
        self,
        query: str,
        embedding: QueryEmbedding | None = None,
    ) -> ContextBundle:
        return ContextBundle(
            id=ContextBundleId(value=self._uuid_provider()),
            query=query,
            embedding=embedding,
        )

    def create_document(
        self,
        content: str,
        score: SimilarityScore,
    ) -> RetrievedDocument:
        return RetrievedDocument(
            id=RetrievedDocumentId(value=self._uuid_provider()),
            content=content,
            score=score,
        )
