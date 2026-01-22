from vulnfinder.domain.analysis.entities.core import (
    AnalysisRun,
    AnalysisTarget,
    AnalysisTask,
)
from vulnfinder.domain.analysis.value_objects.identifiers import (
    AnalysisRunId,
    AnalysisTargetId,
    AnalysisTaskId,
)
from vulnfinder.domain.analysis.value_objects.types import (
    AnalysisConfig,
    AnalysisStatus,
    AnalysisTargetType,
)
from vulnfinder.domain.codebase.value_objects.types import FilePath, ProgrammingLanguage
from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService


class AnalysisFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider = uuid_provider

    def create_run(self, config: AnalysisConfig) -> AnalysisRun:
        return AnalysisRun(
            id=AnalysisRunId(value=self._uuid_provider()),
            status=AnalysisStatus(value="CREATED"),
            config=config,
        )

    def create_target(
        self,
        path: FilePath,
        target_type: AnalysisTargetType,
        language: ProgrammingLanguage | None = None,
    ) -> AnalysisTarget:
        return AnalysisTarget(
            id=AnalysisTargetId(value=self._uuid_provider()),
            path=path,
            target_type=target_type,
            language=language,
        )

    def create_task(self, target_id: AnalysisTargetId) -> AnalysisTask:
        return AnalysisTask(
            id=AnalysisTaskId(value=self._uuid_provider()),
            target_id=target_id,
            status=AnalysisStatus(value="CREATED"),
        )
