import os
from pydantic import BaseModel, Field

from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig

class ApplicationConfig(BaseModel):
    chromadb_vector_store: ChromaDBVectorStoreConfig = Field(
        default_factory=lambda: ChromaDBVectorStoreConfig(**os.environ),
        description="Chroma DB settings"
    )
    open_router_config: OpenRouterConfig = Field(
        default_factory=lambda: OpenRouterConfig(**os.environ),
        description="Open Router settings"
    )
