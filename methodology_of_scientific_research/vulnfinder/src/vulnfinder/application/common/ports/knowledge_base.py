from abc import abstractmethod
from typing import Protocol

from vulnfinder.application.common.models.knowledge_base_state import KnowledgeBaseState


class KnowledgeBaseMetadataStore(Protocol):
    @abstractmethod
    def load(self) -> KnowledgeBaseState:
        raise NotImplementedError

    @abstractmethod
    def save(self, state: KnowledgeBaseState) -> None:
        raise NotImplementedError


class KnowledgeBaseUpdater(Protocol):
    @abstractmethod
    def update(self) -> KnowledgeBaseState:
        raise NotImplementedError
