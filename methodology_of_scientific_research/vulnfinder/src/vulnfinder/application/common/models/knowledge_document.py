from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    content: str
    metadata: dict[str, str]

