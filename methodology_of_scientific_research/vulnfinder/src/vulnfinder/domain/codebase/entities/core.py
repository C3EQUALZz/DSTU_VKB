from dataclasses import dataclass

from vulnfinder.domain.codebase.value_objects.identifiers import CodeArtifactId, CodeSnippetId
from vulnfinder.domain.codebase.value_objects.types import FilePath, LineRange, ProgrammingLanguage
from vulnfinder.domain.common.entities.base_aggregate import BaseAggregateRoot
from vulnfinder.domain.common.entities.base_entity import BaseEntity


@dataclass(eq=False, kw_only=True)
class CodeArtifact(BaseAggregateRoot[CodeArtifactId]):
    path: FilePath
    is_directory: bool
    language: ProgrammingLanguage | None = None


@dataclass(eq=False, kw_only=True)
class CodeSnippet(BaseEntity[CodeSnippetId]):
    artifact_id: CodeArtifactId
    content: str
    location: LineRange

