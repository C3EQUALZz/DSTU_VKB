from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class KnowledgeBaseState:
    document_count: int
    last_updated: datetime | None

