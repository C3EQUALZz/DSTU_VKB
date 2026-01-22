import json
from pathlib import Path

from typing_extensions import override

from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument
from vulnfinder.application.common.ports.knowledge_source import KnowledgeSource


class JsonlKnowledgeSource(KnowledgeSource):
    @override
    def load(self, path: Path) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                payload = json.loads(line)
                content = str(payload.get("content") or payload.get("text") or "")
                if not content:
                    continue
                metadata = payload.get("metadata", {})
                if not isinstance(metadata, dict):
                    metadata = {}
                documents.append(
                    KnowledgeDocument(
                        content=content,
                        metadata={key: str(value) for key, value in metadata.items()},
                    ),
                )
        return documents
