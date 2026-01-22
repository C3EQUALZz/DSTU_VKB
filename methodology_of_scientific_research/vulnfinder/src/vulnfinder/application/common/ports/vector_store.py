from abc import abstractmethod
from typing import Protocol

from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument


class VectorStoreGateway(Protocol):
    @abstractmethod
    def add_documents(self, documents: list[KnowledgeDocument]) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(self, query: str, k: int) -> list[KnowledgeDocument]:
        raise NotImplementedError

    @abstractmethod
    def get_document_count(self) -> int:
        raise NotImplementedError

