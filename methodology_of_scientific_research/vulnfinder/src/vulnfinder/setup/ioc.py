from collections.abc import Iterable
from typing import Final

from dishka import Provider, Scope

from vulnfinder.application.commands.analysis import AnalyzeCodeCommandHandler
from vulnfinder.application.commands.knowledge_base import (
    EnsureKnowledgeBaseCommandHandler,
    IngestDocumentsCommandHandler,
)
from vulnfinder.application.common.ports import (
    KnowledgeBaseMetadataStore,
    KnowledgeBaseUpdater,
    KnowledgeSource,
    VectorStoreGateway,
)
from vulnfinder.application.queries.knowledge_base import SearchKnowledgeBaseQueryHandler
from vulnfinder.domain.analysis.services import AnalysisFactory
from vulnfinder.domain.codebase.services import CodebaseFactory
from vulnfinder.domain.common.ports import UUIDProvider
from vulnfinder.domain.knowledge_base.services import KnowledgeBaseFactory
from vulnfinder.domain.llm_analysis.services import LlmAnalysisFactory
from vulnfinder.domain.rag.services import RagFactory
from vulnfinder.domain.reporting.services import ReportingFactory
from vulnfinder.domain.vulnerability.services import VulnerabilityFactory
from vulnfinder.infrastructure.adapters import (
    ChromaVectorStoreGateway,
    JsonKnowledgeBaseMetadataStore,
    JsonlKnowledgeSource,
    NvdKnowledgeBaseUpdater,
    Uuid4Provider,
)
from vulnfinder.infrastructure.adapters.providers import (
    create_chromadb_vector_store,
    create_embedding_function,
    create_llm_client,
)
from vulnfinder.setup.configs.knowledge_base_config import KnowledgeBaseConfig
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig


def configs_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.from_context(KnowledgeBaseConfig)
    provider.from_context(OpenRouterConfig)
    provider.from_context(ChromaDBVectorStoreConfig)
    return provider


def domain_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=Uuid4Provider, provides=UUIDProvider)
    provider.provide_all(
        AnalysisFactory,
        CodebaseFactory,
        KnowledgeBaseFactory,
        LlmAnalysisFactory,
        RagFactory,
        ReportingFactory,
        VulnerabilityFactory,
    )
    return provider


def application_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        create_embedding_function,
        create_chromadb_vector_store,
        create_llm_client,
    )
    provider.provide(source=ChromaVectorStoreGateway, provides=VectorStoreGateway)
    provider.provide(source=JsonlKnowledgeSource, provides=KnowledgeSource)
    provider.provide(
        source=JsonKnowledgeBaseMetadataStore,
        provides=KnowledgeBaseMetadataStore,
    )
    provider.provide(source=NvdKnowledgeBaseUpdater, provides=KnowledgeBaseUpdater)
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide_all(
        AnalyzeCodeCommandHandler,
        EnsureKnowledgeBaseCommandHandler,
        IngestDocumentsCommandHandler,
        SearchKnowledgeBaseQueryHandler,
    )
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        domain_ports_provider(),
        application_ports_provider(),
        interactors_provider(),
    )
