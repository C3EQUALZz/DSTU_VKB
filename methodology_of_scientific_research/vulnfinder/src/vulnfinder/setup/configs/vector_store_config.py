from pathlib import Path

from pydantic import BaseModel, Field


class ChromaDBVectorStoreConfig(BaseModel):
    collection_name: str = Field(
        description="The collection name",
        alias="CHROMA_COLLECTION_NAME",
        default="default_collection",
    )
    persist_directory: Path = Field(
        description="The directory to persist the data into",
        alias="CHROMA_PERSIST_DIRECTORY",
    )
