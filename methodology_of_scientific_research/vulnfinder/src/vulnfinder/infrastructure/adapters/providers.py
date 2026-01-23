from langchain_chroma import Chroma
from langchain_core.embeddings.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from vulnfinder.application.common.ports.llm_client import LlmClient
from vulnfinder.infrastructure.adapters.llm.langchain_llm_client import LangChainLlmClient
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig


def create_embedding_function(
    config: OpenRouterConfig,
) -> Embeddings:
    return OpenAIEmbeddings(
        api_key=config.api_key,  # type: ignore[arg-type,unused-ignore,call-arg]
        base_url=config.url,  # type: ignore[call-arg,unused-ignore]
        model=config.embedding_model,
        chunk_size=100,
    )


def create_chromadb_vector_store(
    config: ChromaDBVectorStoreConfig, embedding_function: Embeddings
) -> VectorStore:
    return Chroma(
        collection_name=config.collection_name,
        persist_directory=str(config.persist_directory),
        embedding_function=embedding_function,
    )


def create_llm_client(config: OpenRouterConfig) -> LlmClient:
    chat_model: ChatOpenAI = ChatOpenAI(
        api_key=config.api_key,  # type: ignore[arg-type,unused-ignore]
        base_url=config.url,
        model=config.default_model,
    )

    return LangChainLlmClient(chat_model)
