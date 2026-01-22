from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument


class KnowledgeSource(Protocol):
    @abstractmethod
    def load(self, path: Path) -> list[KnowledgeDocument]:
        raise NotImplementedError
