from typing import Final

from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService
from vulnfinder.domain.knowledge_base.entities.core import CVE, CWE, KnowledgeEntry
from vulnfinder.domain.knowledge_base.value_objects.identifiers import (
    CVEId,
    CWEId,
    KnowledgeEntryId,
)


class KnowledgeBaseFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider: Final[UUIDProvider] = uuid_provider

    def create_cve(self, cve_id: CVEId, summary: str, severity: str | None = None) -> CVE:
        return CVE(
            id=cve_id,
            summary=summary,
            severity=severity,
        )

    def create_cwe(self, cwe_id: CWEId, name: str, description: str) -> CWE:
        return CWE(
            id=cwe_id,
            name=name,
            description=description,
        )

    def create_entry(
        self,
        title: str,
        description: str,
        references: tuple[str, ...] = (),
        tags: tuple[str, ...] = (),
        aliases: tuple[str, ...] = (),
        cve: CVE | None = None,
        cwe: CWE | None = None,
    ) -> KnowledgeEntry:
        return KnowledgeEntry(
            id=KnowledgeEntryId(value=self._uuid_provider()),
            title=title,
            description=description,
            references=references,
            tags=tags,
            aliases=aliases,
            cve=cve,
            cwe=cwe,
        )
