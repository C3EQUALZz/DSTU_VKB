from dataclasses import dataclass

from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity
from vulnfinder.domain.knowledge_base.value_objects.identifiers import CVEId, CWEId, KnowledgeEntryId


@dataclass(eq=False, kw_only=True)
class CVE(BaseEntity[CVEId]):
    summary: str
    published_at: str | None = None
    severity: str | None = None


@dataclass(eq=False, kw_only=True)
class CWE(BaseEntity[CWEId]):
    name: str
    description: str


@dataclass(eq=False, kw_only=True)
class KnowledgeEntry(BaseAggregateRoot[KnowledgeEntryId]):
    title: str
    description: str
    references: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    cve: CVE | None = None
    cwe: CWE | None = None

