from dataclasses import dataclass, field

from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity
from vulnfinder.domain.reporting.value_objects.identifiers import ReportId, ReportItemId
from vulnfinder.domain.reporting.value_objects.types import ReportFormat, ReportSummary
from vulnfinder.domain.vulnerability.value_objects.identifiers import VulnerabilityId


@dataclass(eq=False, kw_only=True)
class ReportItem(BaseEntity[ReportItemId]):
    vulnerability_id: VulnerabilityId | None
    content: str
    severity: str | None = None


@dataclass(eq=False, kw_only=True)
class Report(BaseAggregateRoot[ReportId]):
    format: ReportFormat
    items: list[ReportItem] = field(default_factory=list)
    summary: ReportSummary | None = None

    def add_item(self, item: ReportItem) -> None:
        self.items.append(item)
