import json
from datetime import datetime
from pathlib import Path

from vulnfinder.application.common.models.knowledge_base_state import KnowledgeBaseState
from vulnfinder.application.common.ports.knowledge_base import KnowledgeBaseMetadataStore
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig


class JsonKnowledgeBaseMetadataStore(KnowledgeBaseMetadataStore):
    def __init__(self, config: ChromaDBVectorStoreConfig) -> None:
        self._metadata_path = Path(config.persist_directory) / "knowledge_base.json"

    def load(self) -> KnowledgeBaseState:
        if not self._metadata_path.exists():
            return KnowledgeBaseState(document_count=0, last_updated=None)

        payload = json.loads(self._metadata_path.read_text(encoding="utf-8"))
        last_updated_raw = payload.get("last_updated")
        last_updated = (
            datetime.fromisoformat(last_updated_raw) if isinstance(last_updated_raw, str) else None
        )
        count = int(payload.get("document_count", 0))
        return KnowledgeBaseState(document_count=count, last_updated=last_updated)

    def save(self, state: KnowledgeBaseState) -> None:
        payload = {
            "document_count": state.document_count,
            "last_updated": state.last_updated.isoformat() if state.last_updated else None,
        }
        self._metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self._metadata_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

