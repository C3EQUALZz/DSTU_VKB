from dataclasses import dataclass, field
from datetime import UTC, datetime

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
from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity


@dataclass(eq=False, kw_only=True)
class AnalysisTarget(BaseEntity[AnalysisTargetId]):
    path: FilePath
    target_type: AnalysisTargetType
    language: ProgrammingLanguage | None = None


@dataclass(eq=False, kw_only=True)
class AnalysisTask(BaseEntity[AnalysisTaskId]):
    target_id: AnalysisTargetId
    status: AnalysisStatus
    error_message: str | None = None


@dataclass(eq=False, kw_only=True)
class AnalysisRun(BaseAggregateRoot[AnalysisRunId]):
    status: AnalysisStatus
    config: AnalysisConfig
    targets: list[AnalysisTarget] = field(default_factory=list)
    tasks: list[AnalysisTask] = field(default_factory=list)
    last_error: str | None = None

    def add_target(self, target: AnalysisTarget) -> None:
        self.targets.append(target)
        self._touch()

    def add_task(self, task: AnalysisTask) -> None:
        self.tasks.append(task)
        self._touch()

    def start(self) -> None:
        self.status = AnalysisStatus(value="RUNNING")
        self._touch()

    def finish(self) -> None:
        self.status = AnalysisStatus(value="FINISHED")
        self._touch()

    def fail(self, message: str | None = None) -> None:
        self.status = AnalysisStatus(value="FAILED")
        self.last_error = message
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

