from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService
from vulnfinder.domain.reporting.entities.core import Report, ReportItem
from vulnfinder.domain.reporting.value_objects.identifiers import ReportId, ReportItemId
from vulnfinder.domain.reporting.value_objects.types import ReportFormat, ReportSummary
from vulnfinder.domain.vulnerability.value_objects.identifiers import VulnerabilityId


class ReportingFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider = uuid_provider

    def create_report(self, report_format: ReportFormat) -> Report:
        return Report(
            id=ReportId(value=self._uuid_provider()),
            format=report_format,
        )

    def create_item(
        self,
        content: str,
        vulnerability_id: VulnerabilityId | None = None,
        severity: str | None = None,
    ) -> ReportItem:
        return ReportItem(
            id=ReportItemId(value=self._uuid_provider()),
            vulnerability_id=vulnerability_id,
            content=content,
            severity=severity,
        )

    def create_summary(self, total: int, critical: int, high: int, medium: int, low: int) -> ReportSummary:
        return ReportSummary(total=total, critical=critical, high=high, medium=medium, low=low)
