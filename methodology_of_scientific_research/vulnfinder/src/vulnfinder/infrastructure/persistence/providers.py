from typing import Iterator

from langchain_chroma import Chroma
from langchain_core.embeddings.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig

def create_embedding_function(
       config: OpenRouterConfig,
) -> Embeddings:
    return OpenAIEmbeddings(

    )

def create_chromadb_vector_store(
        config: ChromaDBVectorStoreConfig,
        embedding_function: Embeddings
) -> Iterator[VectorStore]:
    yield Chroma(
        collection_name=config.collection_name,
        persist_directory=str(config.persist_directory),
        embedding_function=embedding_function,
    )
