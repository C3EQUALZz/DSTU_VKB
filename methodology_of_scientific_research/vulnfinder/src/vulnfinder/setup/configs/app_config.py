import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from vulnfinder.setup.configs.knowledge_base_config import KnowledgeBaseConfig
from vulnfinder.setup.configs.logging import LoggingConfig
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig


class ApplicationConfig(BaseModel):
    load_dotenv(
        r"D:\Progrramming\PycharmProjects\DSTU_VKB\methodology_of_scientific_research\vulnfinder\.env"
    )
    load_dotenv(
        r"D:\PycharmProjects\DSTU_VKB\methodology_of_scientific_research\vulnfinder\.env"
    )

    chromadb_vector_store: ChromaDBVectorStoreConfig = Field(
        default_factory=lambda: ChromaDBVectorStoreConfig(**os.environ),
        description="Chroma DB settings",
    )
    open_router_config: OpenRouterConfig = Field(
        default_factory=lambda: OpenRouterConfig(**os.environ),
        description="Open Router settings",
    )
    knowledge_base: KnowledgeBaseConfig = Field(
        default_factory=lambda: KnowledgeBaseConfig(**os.environ),
        description="Knowledge base settings",
    )
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging settings",
    )
