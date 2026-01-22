import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Final, final

from vulnfinder.application.common.models.knowledge_base_state import KnowledgeBaseState
from vulnfinder.application.common.ports.knowledge_base import KnowledgeBaseMetadataStore, KnowledgeBaseUpdater
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class EnsureKnowledgeBaseCommand:
    max_age_days: int = 7
    force_refresh: bool = False


@final
class EnsureKnowledgeBaseCommandHandler:
    def __init__(
        self,
        vector_store: VectorStoreGateway,
        metadata_store: KnowledgeBaseMetadataStore,
        updater: KnowledgeBaseUpdater,
    ) -> None:
        self._vector_store: Final[VectorStoreGateway] = vector_store
        self._metadata_store: Final[KnowledgeBaseMetadataStore] = metadata_store
        self._updater: Final[KnowledgeBaseUpdater] = updater

    def __call__(self, data: EnsureKnowledgeBaseCommand) -> KnowledgeBaseState:
        state = self._metadata_store.load()
        actual_count = self._vector_store.get_document_count()
        if actual_count != state.document_count:
            state = KnowledgeBaseState(document_count=actual_count, last_updated=state.last_updated)

        should_refresh = data.force_refresh or actual_count == 0 or self._is_stale(state, data.max_age_days)
        if should_refresh:
            if actual_count == 0:
                logger.info("Knowledge base is empty. Downloading CVE data and building index.")
            else:
                logger.info("Knowledge base is stale. Updating CVE data and rebuilding index.")
            updated_state = self._updater.update()
            self._metadata_store.save(updated_state)
            return updated_state

        logger.debug("Knowledge base is up-to-date. Skipping update.")
        return state

    @staticmethod
    def _is_stale(state: KnowledgeBaseState, max_age_days: int) -> bool:
        if state.last_updated is None:
            return True
        threshold = datetime.now(UTC) - timedelta(days=max_age_days)
        return state.last_updated < threshold

